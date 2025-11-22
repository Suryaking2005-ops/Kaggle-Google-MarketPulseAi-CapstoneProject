import google.generativeai as genai
from config import GOOGLE_API_KEY, Model_NAME
from logger import setup_logger
from tools import GoogleSearchTool, MarketDataTool, TechnicalAnalysisTool

logger = setup_logger("Agents")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.model = genai.GenerativeModel(Model_NAME)

    def generate_response(self, prompt):
        try:
            logger.info(f"{self.name} is thinking...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"{self.name} failed to generate response: {e}")
            return f"Error generating response: {e}"

class ResearcherAgent(Agent):
    def __init__(self):
        super().__init__("Researcher", "Gather information")
        self.search_tool = GoogleSearchTool()

    def analyze(self, ticker):
        # Clean ticker for search (remove .NS or .BO)
        search_ticker = ticker.replace(".NS", "").replace(".BO", "")
        query = f"latest news and analysis for {search_ticker} stock"
        search_results = self.search_tool.search(query)
        prompt = f"""
        You are a Researcher for an investment committee.
        Analyze the following search results for {search_ticker} ({ticker}):
        {search_results}
        
        Summarize the key news, sentiment, and any major upcoming events.
        Be concise and factual.
        """
        return self.generate_response(prompt)

class QuantAgent(Agent):
    def __init__(self):
        super().__init__("Quant", "Technical Analysis")
        self.market_tool = MarketDataTool()
        self.tech_tool = TechnicalAnalysisTool()

    def analyze(self, ticker):
        data = self.market_tool.get_historical_data(ticker)
        if data.empty:
            return "No data found."
        
        rsi = self.tech_tool.calculate_rsi(data)
        volatility = self.tech_tool.calculate_volatility(data)
        current_price = data['Close'].iloc[-1]
        
        prompt = f"""
        You are a Quant Analyst.
        Here is the data for {ticker}:
        Current Price: {current_price}
        RSI (14-day): {rsi}
        Annualized Volatility: {volatility}
        
        Provide a brief technical assessment based on these metrics.
        Is the stock overbought/oversold? Is it volatile?
        """
        return self.generate_response(prompt)

class RiskAgent(Agent):
    def __init__(self):
        super().__init__("Risk Officer", "Devil's Advocate")

    def analyze(self, ticker, researcher_output, quant_output):
        prompt = f"""
        You are a Risk Officer. Your job is to find reasons NOT to invest.
        
        Researcher's Findings:
        {researcher_output}
        
        Quant's Findings:
        {quant_output}
        
        Identify potential risks, regulatory hurdles, macro headwinds, or contradictions in the data.
        Play the Devil's Advocate.
        """
        return self.generate_response(prompt)

class SynthesizerAgent(Agent):
    def __init__(self):
        super().__init__("Synthesizer", "Final Decision")

    def analyze(self, ticker, researcher_output, quant_output, risk_output):
        prompt = f"""
        You are the Chair of the Investment Committee.
        Synthesize the following reports into a final "Buy", "Hold", or "Sell" recommendation for {ticker}.
        
        Researcher: {researcher_output}
        Quant: {quant_output}
        Risk Officer: {risk_output}
        
        Format your response as a memo:
        1. Recommendation (BUY/HOLD/SELL)
        2. Key Rationale
        3. Risk Factors
        4. Conclusion
        """
        return self.generate_response(prompt)
