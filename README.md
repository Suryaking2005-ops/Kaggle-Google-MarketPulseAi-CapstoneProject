# MarketPulse — Multi‑Agent Investment Analysis System

**MarketPulse** is an institutional‑grade, multi‑agent platform that automates equity research, quantitative modeling, and risk evaluation. By mimicking the workflow of a professional investment committee, the system delegates specialized tasks to independent agents powered by Google Gemini, delivering scalable, consistent, and holistic investment analysis with minimal manual effort.

---

## Table of Contents
- [Problem Overview](#problem-overview)
- [Solution Overview](#solution-overview)
- [System Architecture](#system-architecture)
  - [Core Components](#core-components)
- [Execution Interfaces](#execution-interfaces)
- [Agent Breakdown](#agent-breakdown)
  - [ResearcherAgent](#researcheragent)
  - [QuantAgent](#quantagent)
  - [RiskAgent](#riskagent)
  - [SynthesizerAgent](#synthesizeragent)
- [Tools & Utilities](#tools--utilities)
- [Workflow](#workflow)
- [Setup & Configuration](#setup--configuration)
- [Value Proposition](#value-proposition)
- [Future Enhancements](#future-enhancements)
- [Conclusion](#conclusion)
- [License](#license)

---

## Problem Overview
Equity research in traditional settings is:

- **Labor‑intensive** – analysts must continuously track news, fundamentals, and technical data.
- **Inconsistent** – methodologies vary across analysts and firms.
- **Fragmented** – research, modeling, and risk assessment are often siloed.
- **Time‑consuming** – manual processes can take hours per ticker, limiting coverage.

These challenges reduce the speed and reliability of investment decisions.

---

## Solution Overview
MarketPulse orchestrates a committee of purpose‑built agents that collectively:

| Agent | Role | Core Output |
|-------|------|-------------|
| **ResearcherAgent** | Fundamental & news research | Latest sentiment, event summary, analyst insights |
| **QuantAgent** | Price data & technical analytics | RSI, volatility, historical trend interpretation |
| **RiskAgent** | Downside & adversarial review | Red‑flag risks, macro considerations, contradictions |
| **SynthesizerAgent** | Final investment memo | Buy / Hold / Sell recommendation with supporting rationale |

All outputs are persisted in a JSON‑based memory store, enabling longitudinal tracking of investment calls.

---

## System Architecture
MarketPulse is built as a **modular agent ecosystem** rather than a monolithic model. All agents inherit from a common `Agent` base class that standardizes Gemini interactions, logging, and error handling.

### Core Components

| Module      | Description |
|-------------|-------------|
| **agents.py** | Defines all four specialized agents and their interaction logic |
| **tools.py** | Implements search, market data retrieval, and technical indicator calculations |
| **memory.py** | JSON‑based persistent storage (`memory.json`) for historical assessments |
| **logger.py** | Unified logging to console and file with configurable verbosity |
| **config.py** | Holds API keys, model configurations, and environment constants |

---

## Execution Interfaces
| Interface | Description | Typical Use |
|-----------|-------------|-------------|
| **CLI** (`main.py`) | Command‑line entry point for scripting and batch runs | Automated pipelines, CI/CD integration |
| **Streamlit UI** (`app.py`) | Interactive dashboard for on‑demand analysis and presentation | Human‑in‑the‑loop reviews, demo presentations |

Both interfaces invoke the same agent pipeline in the order **Research → Quant → Risk → Synthesis**, ensuring identical results regardless of entry point.

---

## Agent Breakdown

### ResearcherAgent
- **Purpose:** Gather fundamental data, earnings updates, analyst opinions, and market sentiment.
- **Key Capabilities:**  
  - Exchange‑aware ticker handling (e.g., `.NS`, `.BO`).  
  - Structured event‑driven summary generation.
- **Output Example:**  
  ```json
  {
    "sentiment": "positive",
    "events": ["Q3 earnings beat", "new product launch"],
    "analyst_views": ["Buy rating from Morgan Stanley", "Hold from Barclays"]
  }
  ```

### QuantAgent
- **Purpose:** Retrieve historical price data and compute technical metrics.
- **Data Source:** `yfinance` (OHLCV).
- **Computed Metrics:**  
  - **RSI (14‑period)** – Overbought/oversold status.  
  - **Volatility (21‑day rolling, annualized)** – Price stability and risk.  
  - **Historical trend analysis** – Interpretation of price movement patterns.
- **Output Example:**  
  ```json
  {
    "rsi": 68,
    "rsi_signal": "overbought",
    "volatility": 0.22,
    "trend": "upward consolidation"
  }
  ```

### RiskAgent
- **Purpose:** Perform an adversarial review to surface downside risks.
- **Focus Areas:**  
  - Macro‑economic and regulatory threats.  
  - Structural weaknesses and sector‑specific risks.  
  - Contradictions between quantitative signals and fundamentals.
- **Output Example:**  
  ```json
  {
    "red_flags": ["Supply‑chain constraints", "Increasing interest rates"],
    "macro_risks": ["GDP slowdown in key markets"],
    "contradictions": ["Fundamentals bullish, RSI overbought"]
  }
  ```

### SynthesizerAgent
- **Purpose:** Consolidate all inputs into a concise investment memo.
- **Components of the Memo:**  
  - Thesis summary.  
  - Recommendation (Buy / Hold / Sell).  
  - Supporting factors from research, quant, and risk analyses.  
  - Key risk considerations.
- **Output Example:**  
  ```markdown
  **Recommendation:** BUY  
  **Thesis:** Strong earnings momentum coupled with a solid balance sheet.  
  **Supporting Factors:** Positive sentiment, RSI approaching neutral, low volatility.  
  **Risks:** Potential supply‑chain disruptions; high valuation multiples.
  ```

---

## Tools & Utilities

| Tool | Function | Key Features |
|------|----------|--------------|
| **GoogleSearchTool** | Retrieves structured news and analyst commentary | Handles rate limits, graceful error handling |
| **MarketDataTool** | Fetches historical OHLCV data and company metadata via `yfinance` | Returns `pandas.DataFrame` for downstream analysis |
| **TechnicalAnalysisTool** | Calculates technical metrics | - **RSI** – Momentum positioning <br> - **Volatility** – Price stability & risk |
| **MemoryBank** | Persists analysis results in `memory.json` | Enables performance tracking across time and tickers |

---

## Workflow
```
User Input (Ticker) → ResearcherAgent → QuantAgent → RiskAgent → SynthesizerAgent → Save to MemoryBank
```
Each stage consumes the previous agent’s output, mirroring an investment committee decision flow.

---

## Setup & Configuration

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Update `config.py` with your Google Gemini API key:
```python
GOOGLE_API_KEY = "your_key_here"
```

### 3. Run the CLI
```bash
python main.py --ticker AAPL
```
The command prints the final investment memo and stores the full analysis in `memory.json`.

### 4. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
Use the web UI to select tickers, view intermediate agent outputs, and export reports.

---

## Value Proposition

| Benefit | Impact |
|---------|--------|
| Institutional‑grade research | Enables deep analysis without a large analyst team |
| Consistent, repeatable methodology | Reduces bias and variance across tickers |
| Faster due diligence | Turns hours‑long processes into minutes |
| Historical memory | Tracks performance of past calls for continuous improvement |
| Modular architecture | Simplifies extension with new agents or data sources |

---

## Future Enhancements
- Portfolio‑level optimization agents for asset allocation.  
- Real‑time price ingestion with alerting on threshold events.  
- ESG scoring agent to incorporate sustainability metrics.  
- Broker integration for automated order execution.  

---

## Conclusion
MarketPulse bridges traditional equity research and autonomous AI‑driven decision frameworks. By integrating specialized agents into a unified workflow, the platform delivers scalable, repeatable, and data‑backed investment insights, allowing analysts to shift focus from manual data collection to high‑leverage strategic decision‑making. As markets evolve, MarketPulse positions itself as a future‑ready research stack that augments human judgment, accelerates due diligence, and institutionalizes analytical rigor.

---

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.
