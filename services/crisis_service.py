from config import CRISIS_KEYWORDS

CRISIS_FOOTER = """

💙 I hear that you're going through something really painful.
Please know you're not alone — reach out to someone who can help:

📞 iCall (India): 9152987821
📞 Vandrevala Foundation: 1860-2662-345 (24/7, free)
💬 iCall WhatsApp: wa.me/919152987821"""


def is_crisis(text: str) -> bool:
    return any(kw in text.lower() for kw in CRISIS_KEYWORDS)


def append_footer(reply: str) -> str:
    return reply + CRISIS_FOOTER
