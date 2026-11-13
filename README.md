# Automated Equity & AI Risk Screener

An automated financial risk and investment assessment pipeline for Asset Management built with Python, SQLite, `yfinance`, Pydantic, and the OpenAI API (`gpt-4o-mini`). 

This tool extracts real-time market data, generates structured investment verdicts via LLM function calling, persists analysis results in a local SQLite database, and exports actionable findings for portfolio management into Excel.

---

## Key Features

- **Market Data Extraction:** Dynamically retrieves fundamental stock metrics (Forward P/E, Revenue Growth, Business Summary) using `yfinance`.
- **Structured AI Insights:** Enforces strict output validation using Pydantic (`CompanyAIRating`) with OpenAI Structured Outputs (`client.beta.chat.completions.parse`) for:
  - Top 3 risk factors over a 12-month horizon
  - Investment sentiment verdict (Bullish, Neutral, Bearish)
  - Confidence scoring (1 to 10 scale)
- **Relational Data Persistence (SQLite):** Automatically initializes a local relational database (`ai_asset_screener.db`) to store, update, and manage historical stock analysis records using raw SQL queries (`CREATE TABLE`, `INSERT OR REPLACE`).
- **Portfolio Analytics & Filtering:** Includes custom SQL queries to filter high-confidence bullish recommendations (`confidence_score >= 8`) for portfolio overlay decision-making.
- **Automated Excel Reporting:** Exports aggregated multi-ticker screening results directly into a structured Excel report (`AI_Asset_Management_Analysis.xlsx`).

---

## Tech Stack

- **Language:** Python 3.13+
- **Database:** SQLite3
- **Data & API:** `yfinance`, `pandas`, `openpyxl`
- **Data Validation:** `pydantic`
- **AI Integration:** `openai` (`gpt-4o-mini`), `python-dotenv`

---

## Project Structure

```text
ai-asset-management-screener/
├── models.py           # Pydantic schema for structured AI outputs
├── ai_pipeline.py      # Core yfinance & OpenAI integration logic
├── database.py         # SQLite connection, DDL/DML operations & SQL analytics
├── main.py             # Pipeline orchestrator, database sync & Excel export runner
├── .env.example        # Environment variable template
├── .gitignore          # File exclusion rules for version control (ignoring .env & .db)
└── README.md           # Project documentation


# 1. Clone repository & install dependencies
git clone [https://github.com/caspargrz/ai-asset-management-screener.git](https://github.com/caspargrz/ai-asset-management-screener.git)
cd ai-asset-management-screener
pip install yfinance pandas openpyxl pydantic openai python-dotenv

# 2. Configure API key
cp .env.example .env
# Add your OPENAI_API_KEY inside .env

# 3. Run screening pipeline
python main.py