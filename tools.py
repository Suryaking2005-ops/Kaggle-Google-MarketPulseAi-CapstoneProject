import yfinance as yf
import pandas as pd
import numpy as np
from googlesearch import search
from logger import setup_logger

logger = setup_logger("Tools")

class GoogleSearchTool:
    def search(self, query, num_results=5):
        """Performs a Google search and returns a list of URLs."""
        try:
            logger.info(f"Searching for: {query}")
            results = list(search(query, num_results=num_results, advanced=True))
            # Extract title and description if possible, otherwise just return results
            formatted_results = []
            for result in results:
                formatted_results.append(f"Title: {result.title}\nDescription: {result.description}\nURL: {result.url}\n")
            return "\n".join(formatted_results)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return f"Search failed: {e}"

class MarketDataTool:
    def get_historical_data(self, ticker, period="1y"):
        """Fetches historical data for a ticker."""
        try:
            logger.info(f"Fetching data for {ticker} over {period}")
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            logger.error(f"Failed to fetch market data: {e}")
            return pd.DataFrame()

    def get_info(self, ticker):
        """Fetches basic info for a ticker."""
        try:
            stock = yf.Ticker(ticker)
            return stock.info
        except Exception as e:
            logger.error(f"Failed to fetch ticker info: {e}")
            return {}

class TechnicalAnalysisTool:
    def calculate_rsi(self, data, window=14):
        """Calculates RSI for the given data."""
        try:
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] # Return the latest RSI
        except Exception as e:
            logger.error(f"RSI calculation failed: {e}")
            return None

    def calculate_volatility(self, data, window=21):
        """Calculates annualized volatility."""
        try:
            daily_returns = data['Close'].pct_change()
            volatility = daily_returns.rolling(window=window).std() * np.sqrt(252)
            return volatility.iloc[-1] # Return latest volatility
        except Exception as e:
            logger.error(f"Volatility calculation failed: {e}")
            return None
