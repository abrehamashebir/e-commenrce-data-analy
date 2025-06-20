import re
import pandas as pd
from config.paths import paths
from typing import List, Tuple

class AmharicPreprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize Amharic text"""
        if not isinstance(text, str):
            return ""
        
        # Normalize Amharic characters
        text = text.replace("ሃ", "ሀ").replace("ሐ", "ሀ").replace("ሓ", "ሀ")
        text = text.replace("ኅ", "ሀ").replace("ኻ", "ሀ")
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def extract_entities(text: str) -> List[Tuple[str, str]]:
        """Basic rule-based entity extraction (for initial labeling)"""
        # Implement your custom rules here
        return []

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df['clean_text'] = df['text'].apply(self.clean_text)
        return df