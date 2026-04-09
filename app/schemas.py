from typing import Literal

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1, description="Text to summarize")
    max_length: int = Field(
        ge=20, le=1000, description="Maximum summary length in characters"
    )


class SummarizeResponse(BaseModel):
    summary: str


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1, description="Text to analyze")


class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str
