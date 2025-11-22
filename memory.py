import json
import os
from config import MEMORY_FILE
from logger import setup_logger

logger = setup_logger("MemoryBank")

class MemoryBank:
    def __init__(self, filepath=MEMORY_FILE):
        self.filepath = filepath
        self.data = self._load_memory()

    def _load_memory(self):
        if not os.path.exists(self.filepath):
            return {"tickers": {}}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode {self.filepath}. Starting with empty memory.")
            return {"tickers": {}}

    def _save_memory(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    def get_ticker_data(self, ticker):
        return self.data["tickers"].get(ticker, {})

    def update_ticker_data(self, ticker, key, value):
        if ticker not in self.data["tickers"]:
            self.data["tickers"][ticker] = {}
        self.data["tickers"][ticker][key] = value
        self._save_memory()
        logger.info(f"Updated memory for {ticker}: {key}")

    def get_all_tickers(self):
        return list(self.data["tickers"].keys())
