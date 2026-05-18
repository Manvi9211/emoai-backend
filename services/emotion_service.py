from transformers import pipeline

print("Loading emotion model... (first run ~30s, cached after)")
_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)
print("Emotion model ready!")


def detect(text: str) -> dict:
    results = _classifier(text[:512])
    sorted_emotions = sorted(
        results[0], key=lambda x: x["score"], reverse=True)
    return {
        "label": sorted_emotions[0]["label"].lower(),
        "score": round(sorted_emotions[0]["score"], 3),
        "all": [
            {"emotion": e["label"].lower(), "score": round(e["score"], 3)}
            for e in sorted_emotions
        ],
    }
