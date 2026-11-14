# Automated Equity & AI Risk Screener

An automated ETL and GenAI equity screening pipeline built to support fundamental research and structured risk assessment in an institutional asset management workflow.

## Overview
This pipeline automates the initial screening of a configurable equity universe (`NVDA`, `AAPL`, `MSFT`, `GOOGL`, `AMZN`) by combining live financial market data with deterministic LLM-based risk analysis. Instead of parsing unstructured text, it enforces strict schema validation via **Pydantic** and persists historical ratings in a local **SQLite** database for quantitative filtering and Excel reporting.

## Architecture & Pipeline Workflow
1. **Market Data Extraction (`yfinance`):** Retrieves real-time valuation multiples (Forward P/E), revenue growth rates, and business descriptions.
2. **Structured AI Risk Assessment (`OpenAI API` + `Pydantic`):** Evaluates each company using `gpt-4o-mini` (`temperature=0.2`) and `client.beta.chat.completions.parse()` against the `CompanyAIRating` Pydantic schema to generate:
   - Concise business summary
   - Top 3 company-specific 12-month risk factors
   - Deterministic investment verdict (`Bullish`, `Neutral`, or `Bearish`)
   - Quantitative confidence score (`1–10`)
3. **Relational Persistence & SQL Filtering (`SQLite3`):** Stores and updates screening results in `ai_asset_screener.db` (`INSERT OR REPLACE`) and queries high-conviction opportunities (`investment_verdict = 'Bullish' AND confidence_score >= 8`).
4. **Committee Reporting (`pandas` + `openpyxl`):** Exports the consolidated screening results into `AI_Asset_Management_Analysis.xlsx`.

## Tech Stack
- **Language:** Python 3.11+
- **Data & Analytics:** `yfinance`, `pandas`, `openpyxl`
- **GenAI & Schema Validation:** `openai` (`gpt-4o-mini` Structured Outputs), `pydantic`
- **Database:** `sqlite3`
- **Configuration:** `python-dotenv`

## Project Structure
```text
ai-asset-screener/
├── assets/
│   ├── code_architecture.png          # Pydantic CompanyAIRating schema
│   ├── excel_report.png               # Formatted Excel committee report
│   └── terminal_output.png            # Pipeline execution & SQL query output
├── .env.example                       # Environment variable template
├── .gitignore
├── ai_asset_screener.db               # SQLite database storing screening results
├── AI_Asset_Management_Analysis.xlsx  # Generated multi-ticker Excel report
├── ai_pipeline.py                     # yfinance extraction & OpenAI structured parsing
├── database.py                        # SQLite schema initialization, upsert & SQL queries
├── main.py                            # End-to-end pipeline orchestration & Excel export
├── models.py                          # Pydantic data validation models
└── README.md

## Setup & Usage

```bash
# 1. Clone repository & install dependencies
git clone [https://github.com/caspargrz/ai-asset-management-screener.git](https://github.com/caspargrz/ai-asset-management-screener.git)
cd ai-asset-management-screener
pip install yfinance pandas openpyxl pydantic openai python-dotenv

# 2. Configure API key
cp .env.example .env
# Add your OPENAI_API_KEY inside .env

# 3. Run screening pipeline
python main.py