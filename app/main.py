import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI

from app.schemas import SentimentRequest, SentimentResponse, SummarizeRequest, SummarizeResponse

load_dotenv()

app = FastAPI(title="FastAPI LLM API")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest) -> SummarizeResponse:
    try:
        response = _client().responses.create(
            model=OPENAI_MODEL,
            input=(
                "Summarize the following text clearly and concisely. "
                f"Keep the summary under {payload.max_length} characters.\n\n"
                f"Text:\n{payload.text}"
            ),
        )
        summary = response.output_text.strip()
        return SummarizeResponse(summary=summary)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {exc}") from exc


@app.post("/analyze-sentiment", response_model=SentimentResponse)
def sentiment(payload: SentimentRequest) -> SentimentResponse:
    try:
        response = _client().responses.create(
            model=OPENAI_MODEL,
            input=(
                "Analyze sentiment and return JSON only with keys: "
                "sentiment (positive|negative|neutral), confidence (0-1 float), explanation.\n\n"
                f"Text:\n{payload.text}"
            ),
        )
        content = response.output_text.strip()
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("Model did not return valid JSON.")

        data = json.loads(content[start : end + 1])
        result = {
            "sentiment": str(data["sentiment"]).lower(),
            "confidence": float(data["confidence"]),
            "explanation": data["explanation"],
        }
        return SentimentResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {exc}") from exc
