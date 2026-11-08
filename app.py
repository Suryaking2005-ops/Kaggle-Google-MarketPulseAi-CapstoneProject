import streamlit as st
from marketpulse.config import MissingAPIKeyError
from marketpulse.agents import ResearcherAgent, QuantAgent, RiskAgent, SynthesizerAgent
from marketpulse.memory import MemoryBank
from marketpulse.logger import setup_logger

# Initialize logger
logger = setup_logger("MarketPulse-UI")

# Streamlit Page Setup
st.set_page_config(page_title="MarketPulse | Investment Committee Bot", layout="wide")
st.title("📈 MarketPulse - Investment Committee Bot")
st.write("Run multi-agent institutional-grade equity analysis.")

# Input Section
col1, col2 = st.columns([1, 3])
with col1:
    exchange = st.radio("Select Exchange", ["US", "NSE", "BSE"])
with col2:
    ticker_input = st.text_input("Enter Stock Ticker (e.g., AAPL, RELIANCE, TCS)").upper()

run_button = st.button("Run Analysis")

if run_button:
    if not ticker_input:
        st.error("Please enter a valid ticker to proceed.")
    else:
        # Handle Exchange Suffixes
        if exchange == "NSE":
            ticker = f"{ticker_input}.NS"
        elif exchange == "BSE":
            ticker = f"{ticker_input}.BO"
        else:
            ticker = ticker_input

        # Initialize Memory & Agents
        memory = MemoryBank()
        try:
            researcher = ResearcherAgent()
            quant = QuantAgent()
            risk_officer = RiskAgent()
            synthesizer = SynthesizerAgent()
        except MissingAPIKeyError as e:
            st.error(str(e))
            st.stop()

        st.info(f"🚀 Running analysis for *{ticker}*...")
        logger.info(f"Starting analysis for {ticker} via UI...")

        # Step 1: Research
        with st.spinner("Researcher Agent analyzing fundamentals..."):
            researcher_output = researcher.analyze(ticker)
        st.subheader("📌 Research Findings")
        st.write(researcher_output)

        # Step 2: Quant
        with st.spinner("Quant Agent running financial models..."):
            quant_output = quant.analyze(ticker)
        st.subheader("📊 Quantitative Analysis")
        st.write(quant_output)

        # Step 3: Risk Assessment
        with st.spinner("Risk Officer assessing downside scenarios..."):
            risk_output = risk_officer.analyze(ticker, researcher_output, quant_output)
        st.subheader("⚠ Risk Evaluation")
        st.write(risk_output)

        # Step 4: Memo
        with st.spinner("Synthesizing final investment memo..."):
            final_memo = synthesizer.analyze(
                ticker, researcher_output, quant_output, risk_output
            )
        st.subheader("📄 Final Investment Memo")
        st.write(final_memo)

        # Save Memory
        memory.update_ticker_data(ticker, "latest_memo", final_memo)
        logger.info(f"Analysis saved in memory for {ticker}")

        st.success("✔ Analysis complete & stored in memory.")