import requests
from fastapi import HTTPException
from os import getenv

HF_TOKEN = getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def detect(text: str):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": text},
            timeout=30
        )

        data = response.json()

        if isinstance(data, dict) and data.get("error"):
            raise HTTPException(status_code=500, detail=data["error"])

        result = data[0]

        best = max(result, key=lambda x: x["score"])

        return {
            "label": best["label"],
            "score": round(best["score"], 3)
        }

    except Exception:
        return {
            "label": "neutral",
            "score": 0.5
        }
