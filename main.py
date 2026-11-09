import pandas as pd

from ai_pipeline import analyze_stock_with_ai


def run_screener(tickers: list[str]):
    results = []
    print("Starting AI analysis for Asset Management...")

    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        try:
            data = analyze_stock_with_ai(ticker)
            results.append(data)
        except Exception as exc:
            print(f"Error analyzing {ticker}: {exc}")

    if not results:
        print("No results were generated. Please check the tickers and try again.")
        return None

    df = pd.DataFrame(results)
    df['top_3_risks'] = df['top_3_risks'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    df = df[['ticker', 'investment_verdict', 'confidence_score', 'top_3_risks', 'buisness_summary']]

    output_file = "AI_Asset_Management_Analysis.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Analysis complete. Results saved to {output_file}")
    return df


if __name__ == "__main__":
    tickers = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN"]
    run_screener(tickers)

