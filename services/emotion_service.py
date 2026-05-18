from transformers import pipeline

print("Loading emotion model... (first run ~30s, cached after)")
_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)
print("Emotion model ready!")


def detect(text: str):
    return {
        "label": "neutral",
        "score": 0.90
    }
