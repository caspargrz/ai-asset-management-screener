import json
import sqlite3

DB_NAME = "ai_asset_screener.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_ai_ratings (
            ticker TEXT PRIMARY KEY,
            investment_verdict TEXT,
            confidence_score INTEGER,
            top_3_risks TEXT,
            business_summary TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_analysis(data: dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    risks_str = json.dumps(data.get("top_3_risks", []))
    cursor.execute(
        """
        INSERT OR REPLACE INTO company_ai_ratings (
            ticker, investment_verdict, confidence_score, top_3_risks, business_summary
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["ticker"],
            data["investment_verdict"],
            data["confidence_score"],
            risks_str,
            data["business_summary"],
        ),
    )
    conn.commit()
    conn.close()


def get_high_confidence_bulls(min_confidence: int = 8) -> list:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT ticker, investment_verdict, confidence_score, top_3_risks
        FROM company_ai_ratings
        WHERE investment_verdict = 'Bullish' AND confidence_score >= ?
        ORDER BY confidence_score DESC
        """,
        (min_confidence,),
    )
    results = cursor.fetchall()
    conn.close()
    return results