import re

CAPS_TOKEN = re.compile(r"^[A-Z0-9:]+(?:\s?[0-9]+)?$")

def is_caps_token(item: str) -> bool:
    return bool(CAPS_TOKEN.match(item.strip()))

def is_race_phrase(item: str) -> bool:
    lower = item.lower()
    return "indian" in lower or "african american" in lower

def split_entry(line: str):
    return [chunk.strip() for chunk in line.split(",") if chunk.strip()]
