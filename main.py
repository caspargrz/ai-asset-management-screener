import pandas as pd
from ai_pipeline import analyze_stock_with_ai
from database import get_high_confidence_bulls, init_db, save_analysis


def run_screener(tickers: list[str]):
   
    init_db()

    results = []
    print("Starting AI analysis for Asset Management...")

    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        try:
            data = analyze_stock_with_ai(ticker)
            results.append(data)

            
            save_analysis(data)

        except Exception as exc:
            print(f"Error analyzing {ticker}: {exc}")

    if not results:
        print(
            "No results were generated. Please check the tickers and try again."
        )
        return None

   
    df = pd.DataFrame(results)
    df["top_3_risks"] = df["top_3_risks"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else x
    )

    output_file = "AI_Asset_Management_Analysis.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Analysis complete. Results saved to {output_file}")

    # 4. Beispiel für SQL-Filterausgabe in der Konsole
    print("\n--- SQL Query: High Confidence Bullish Verdicts (>= 8) ---")
    bulls = get_high_confidence_bulls(min_confidence=8)
    for row in bulls:
        print(
            f"Ticker: {row[0]} | Verdict: {row[1]} | Confidence: {row[2]}/10"
        )

    return df


if __name__ == "__main__":
    tickers = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN"]
    run_screener(tickers)