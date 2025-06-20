import asyncio
from datetime import datetime
from pathlib import Path
import pandas as pd
from telethon import TelegramClient

class TelegramScraper:
    def __init__(self, api_id: str, api_hash: str):
        self.client = TelegramClient('session', api_id, api_hash)
        self.output_dir = Path('data/raw')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def scrape_channel(self, channel: str, limit: int = 100) -> pd.DataFrame:
        """Scrape messages from a single channel"""
        messages = []
        async for msg in self.client.iter_messages(channel, limit=limit):
            messages.append({
                'channel': channel,
                'message_id': msg.id,
                'date': msg.date,
                'views': msg.views,
                'text': msg.text,
                'has_media': bool(msg.media)
            })
        return pd.DataFrame(messages)

    def save_to_csv(self, df: pd.DataFrame) -> str:
        """Save DataFrame to timestamped CSV file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"telegram_{timestamp}.csv"
        filepath = self.output_dir / filename
        df.to_csv(filepath, index=False)
        return str(filepath)

async def main():
    scraper = TelegramScraper(
        api_id='23735929',
        api_hash='36c1864894007dcb935128b3252887a9'
    )
    
    channels = ['ZemenExpress', 'nevacomputer', 'meneshayeofficial']
    all_data = pd.DataFrame()

    async with scraper.client:
        for channel in channels:
            channel_data = await scraper.scrape_channel(channel, limit=100)
            all_data = pd.concat([all_data, channel_data])
        
        saved_path = scraper.save_to_csv(all_data)
        print(f"Data successfully saved to: {saved_path}")

if __name__ == "__main__":
    asyncio.run(main())