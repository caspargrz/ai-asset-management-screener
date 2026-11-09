from pydantic import BaseModel, Field


class CompanyAIRating(BaseModel):
    ticker: str = Field(description="The ticker symbol of the company", examples=["NVDA"])
    buisness_summary: str = Field(description="A brief summary of the company's business")
    top_3_risks: list[str] = Field(description="A list of the top 3 risks for the company in the next 12 months")
    investment_verdict: str = Field(description="Assessment: Bullish, Neutral or Bearish")
    confidence_score: int = Field(description="Confidence score of the AI from 1 to 10", ge=1, le=10)
