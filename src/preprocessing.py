import pandas as pd
import re
from pathlib import Path
from datetime import datetime
import numpy as np
from typing import List, Dict, Optional

class TelegramDataPreprocessor:
    def __init__(self, raw_data_path: str):
        """
        Initialize preprocessor with path to raw CSV data
        """
        self.raw_data = pd.read_csv(raw_data_path)
        self.processed_dir = Path('data/processed')
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Amharic-specific normalization rules
        self.amharic_normalization_map = {
            'ሃ': 'ሀ', 'ሐ': 'ሀ', 'ሓ': 'ሀ', 'ኅ': 'ሀ', 'ኻ': 'ሀ',
            'ኽ': 'ሀ', 'ሀ': 'ሀ', 'ሁ': 'ሁ', 'ኁ': 'ሁ'  # Expand as needed
        }
        
        # Ethiopian currency regex patterns
        self.price_patterns = [
            r'(ዋጋ|በ|ብር|br|birr|price)[:\s]*([\d,]+\.?\d*)',
            r'([\d,]+\.?\d*)\s*(ብር|br|birr)'
        ]

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text with Amharic-specific rules
        """
        if not isinstance(text, str):
            return ""
        
        # Normalize Amharic character variants
        for variant, standard in self.amharic_normalization_map.items():
            text = text.replace(variant, standard)
        
        # Remove unwanted characters (except Amharic, English, and punctuation)
        text = re.sub(r'[^\w\s\u1200-\u137F\.\,\!\?]', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def extract_prices(self, text: str) -> List[float]:
        """
        Extract numeric price values from text using Amharic and English patterns
        """
        if not isinstance(text, str):
            return []
        
        prices = []
        for pattern in self.price_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Choose the right group depending on matched pattern
                    amount_str = match.group(2 if 'ዋጋ' in match.group(0) else 1)
                    amount = float(amount_str.replace(',', ''))
                    prices.append(amount)
                except (ValueError, IndexError):
                    continue
        return prices

    def detect_product_terms(self, text: str) -> List[str]:
        """
        Detect and return product-related keywords from text
        """
        if not isinstance(text, str):
            return []
        
        product_terms = []
        terms = re.findall(r'(\b[\w\u1200-\u137F]+\b)', text)
        
        product_keywords = {
            'ሸክላ', 'ቴሌቪዥን', 'tv', 'phone', 'ስልክ', 
            'laptop', 'ኮምፒውተር', 'shoe', 'ሲሊኮን', 'silicon'
        }
        
        for term in terms:
            if term.lower() in product_keywords:
                product_terms.append(term)
        
        return product_terms

    def preprocess_data(self) -> pd.DataFrame:
        """
        Execute full preprocessing pipeline: clean, extract, enrich
        """
        df = self.raw_data.copy()
        
        # Drop rows with no text
        df = df[df['text'].notna()]
        
        # Clean and normalize
        df['clean_text'] = df['text'].apply(self.clean_text)
        
        # Price extraction
        df['prices'] = df['text'].apply(self.extract_prices)
        df['price_count'] = df['prices'].apply(len)
        df['avg_price'] = df['prices'].apply(lambda x: np.mean(x) if x else np.nan)
        
        # Product keyword detection
        df['product_terms'] = df['clean_text'].apply(self.detect_product_terms)
        df['product_count'] = df['product_terms'].apply(len)
        
        # Date parsing
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['day_of_week'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        
        # Drop short or empty messages
        df['text_length'] = df['clean_text'].apply(len)
        df = df[df['text_length'] > 5]
        
        return df

    def save_processed_data(self, df: pd.DataFrame) -> str:
        """
        Save processed DataFrame to CSV with a timestamped filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"processed_{timestamp}.csv"
        filepath = self.processed_dir / filename
        df.to_csv(filepath, index=False)
        return str(filepath)


# === Example Usage ===
if __name__ == "__main__":
    # Replace with actual CSV file path
    preprocessor = TelegramDataPreprocessor('./data/raw/telegram_20250620_235851.csv')
    
    # Run pipeline
    processed_data = preprocessor.preprocess_data()
    
    # Save and preview
    saved_path = preprocessor.save_processed_data(processed_data)
    print(f"\n✅ Processed data saved to: {saved_path}")
    print("\n📋 Sample Output:")
    print(processed_data[['clean_text', 'avg_price', 'product_terms']].head().to_string())
