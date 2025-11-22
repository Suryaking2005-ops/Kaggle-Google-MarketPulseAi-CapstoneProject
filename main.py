import argparse
import sys
from agents import ResearcherAgent, QuantAgent, RiskAgent, SynthesizerAgent
from memory import MemoryBank
from logger import setup_logger

logger = setup_logger("Main")

def main():
    parser = argparse.ArgumentParser(description="MarketPulse - Institutional Investment Committee Bot")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker symbol (e.g., AAPL)")
    args = parser.parse_args()
    
    ticker = args.ticker.upper()
    logger.info(f"Starting analysis for {ticker}...")

    # Initialize Memory
    memory = MemoryBank()
    
    # Initialize Agents
    researcher = ResearcherAgent()
    quant = QuantAgent()
    risk_officer = RiskAgent()
    synthesizer = SynthesizerAgent()

    # Step 1: Research
    print(f"\n--- Researcher is analyzing {ticker} ---")
    researcher_output = researcher.analyze(ticker)
    print(researcher_output)
    logger.info("Researcher finished.")

    # Step 2: Quant Analysis
    print(f"\n--- Quant is crunching numbers for {ticker} ---")
    quant_output = quant.analyze(ticker)
    print(quant_output)
    logger.info("Quant finished.")

    # Step 3: Risk Assessment
    print(f"\n--- Risk Officer is evaluating {ticker} ---")
    risk_output = risk_officer.analyze(ticker, researcher_output, quant_output)
    print(risk_output)
    logger.info("Risk Officer finished.")

    # Step 4: Synthesis
    print(f"\n--- Synthesizer is drafting the memo ---")
    final_memo = synthesizer.analyze(ticker, researcher_output, quant_output, risk_output)
    print("\n" + "="*40)
    print(final_memo)
    print("="*40 + "\n")
    logger.info("Synthesizer finished.")

    # Save to Memory
    memory.update_ticker_data(ticker, "latest_memo", final_memo)
    logger.info(f"Analysis saved to memory for {ticker}.")

if __name__ == "__main__":
    main()
