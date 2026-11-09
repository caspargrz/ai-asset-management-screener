import os
import yfinance as yf
from dotenv import load_dotenv
from models import CompanyAIRating
from openai import OpenAI

load_dotenv()

client = OpenAI()


def analyze_stock_with_ai(ticker_symbol: str) -> dict:
    stock = yf.Ticker(ticker_symbol)
    info = stock.info

    company_name = info.get("longName", ticker_symbol)
    pe_ratio = info.get("forwardPE", "N/A")
    revenue_growth = info.get("revenueGrowth", "N/A")
    summary = info.get("longBusinessSummary", "")[:800]

    prompt = f"""
    Analyze the following company for an asset management committee:
    - Ticker Symbol: {ticker_symbol}
    - Company Name: {company_name}
    - Forward P/E Ratio: {pe_ratio}
    - Revenue Growth: {revenue_growth}
    - Summary: {summary}
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a very precise and detail oriented financial risk"
                    " analyst providing insights for an asset management"
                    " committee."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        response_format=CompanyAIRating,
        temperature=0.2,
    )

    return response.choices[0].message.parsed.model_dump()


if __name__ == "__main__":
    target_ticker = "GOOGL"
    print(f"Start AI-analysis for {target_ticker}...")
    result = analyze_stock_with_ai(target_ticker)

    print("\n--- analysis-result ---")
    print(result)