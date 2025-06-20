import pandas as pd
from telethon.sync import TelegramClient
from config.paths import paths
from typing import List, Optional
import logging

class TelegramScraper:
    def __init__(self, api_id: str, api_hash: str, channels: List[str]):
        self.client = TelegramClient('session', api_id, api_hash)
        self.channels = channels
        
    async def _scrape_channel(self, channel: str, limit: int = 1000):
        messages = []
        async for message in self.client.iter_messages(channel, limit=limit):
            messages.append({
                'channel': channel,
                'message_id': message.id,
                'date': message.date,
                'views': message.views,
                'text': message.text,
                'media': bool(message.media)
            })
        return messages
    
    async def scrape_all(self, limit: Optional[int] = None):
        all_messages = []
        for channel in self.channels:
            try:
                messages = await self._scrape_channel(channel, limit)
                all_messages.extend(messages)
                logging.info(f"Scraped {len(messages)} messages from {channel}")
            except Exception as e:
                logging.error(f"Error scraping {channel}: {str(e)}")
        return pd.DataFrame(all_messages)
    
    def save_raw_data(self, df: pd.DataFrame, filename: str = "telegram_data.csv"):
        path = paths.RAW_DATA / filename
        df.to_csv(path, index=False)
        logging.info(f"Saved raw data to {path}")