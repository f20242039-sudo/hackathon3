"""
extractor/ai_extractor.py

Converts unstructured natural-language text into structured travel data.

Runtime: Ollama (CPU-only), running a small local model e.g. `llama3.2:1b`
or `qwen2.5:1.5b-instruct`. No GPU/CUDA used. No network calls beyond
localhost (Ollama runs on http://localhost:11434 on the same machine),
so this works fully offline once the model is pulled.

If Ollama is not running / not installed / times out, we fall back to a
deterministic rule-based extractor (keyword + regex matching against a
known vocabulary of Hyderabad places/food/activities). This guarantees
the demo never breaks, and is itself a valid "CPU-only offline" approach.
"""
import json
import re
from typing import Optional

import requests

from chalo_backend.models.schemas import ExtractedData, GroupInfo

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:latest"   # matches `ollama list` on this machine
OLLAMA_TIMEOUT_SECONDS = 45  # llama3.1 is ~8B params -- slower on CPU than a 1B model

SYSTEM_PROMPT = """You are a strict information-extraction engine for a Hyderabad travel app.
Read the user's text and output ONLY valid JSON (no markdown, no explanation) matching this schema:

{
  "places": [string],
  "food": [string],
  "activities": [string],
  "interests": [string],
  "budget": number or null,
  "duration": string or null,
  "group": {"type": string or null, "size": number or null} or null
}

Rules:
- Extract only what is explicitly stated or strongly implied.
- "places" = named tourist spots/landmarks (e.g. Charminar, Golconda Fort).
- "food" = dishes or cuisines mentioned (e.g. Biryani, Haleem).
- "activities" = actions like shopping, sightseeing, boating.
- "interests" = themes like photography, history, nightlife, nature.
- budget = total rupee amount mentioned, else null.
- duration = e.g. "2 Days", else null.
- group.type = Friends/Family/Couple/Solo, group.size = number of people.
- If a field is unknown, use null or an empty list. Do not invent data.
Return ONLY the JSON object.
"""


# ---------------------------------------------------------------------------
# Fallback rule-based extractor (always available, zero dependencies)
# ---------------------------------------------------------------------------

KNOWN_PLACES = [
    "charminar", "golconda fort", "golconda", "chowmahalla palace",
    "laad bazaar", "hussain sagar", "ramoji film city", "qutb shahi tombs",
    "salar jung museum", "birla mandir", "necklace road", "shilparamam",
    "nehru zoological park", "kbr park", "falaknuma palace", "taramati baradari",
    "paigah tombs", "snow world", "hitech city", "gachibowli",
]

KNOWN_FOOD = [
    "biryani", "haleem", "kebab", "kebabs", "irani chai", "osmania biscuit",
    "double ka meetha", "qubani ka meetha", "mirchi bajji", "nihari",
]

KNOWN_ACTIVITIES = [
    "shopping", "sightseeing", "boating", "trekking", "photography walk",
    "nightlife", "museum visit", "temple visit",
]

KNOWN_INTERESTS = [
    "photography", "history", "nature", "art", "architecture",
    "nightlife", "food", "culture", "shopping",
]

GROUP_TYPES = ["friends", "family", "couple", "solo", "colleagues"]


def _rule_based_extract(text: str) -> ExtractedData:
    lower = text.lower()

    places = [p.title() for p in KNOWN_PLACES if p in lower]
    food = [f.title() for f in KNOWN_FOOD if f in lower]
    activities = [a.title() for a in KNOWN_ACTIVITIES if a in lower]
    interests = [i.title() for i in KNOWN_INTERESTS if i in lower and i.title() not in activities]

    # budget: look for ₹/Rs/INR followed by digits, or digits followed by rupee words
    budget = None
    budget_match = re.search(r"(?:₹|rs\.?|inr)\s?([\d,]+)", lower)
    if not budget_match:
        budget_match = re.search(r"([\d,]+)\s?(?:rupees|rs\.?|inr)", lower)
    if budget_match:
        try:
            budget = int(budget_match.group(1).replace(",", ""))
        except ValueError:
            budget = None

    # duration: "2 days", "3-day", "1 week"
    duration = None
    duration_match = re.search(r"(\d+)\s?-?\s?(day|days|night|nights|week|weeks)", lower)
    if duration_match:
        num, unit = duration_match.groups()
        unit_clean = unit.rstrip("s").capitalize()
        plural = "s" if int(num) != 1 else ""
        duration = f"{num} {unit_clean}{plural}"

    # group
    group = None
    group_type_found = next((g for g in GROUP_TYPES if g in lower), None)
    size_match = re.search(r"(\d+)\s?(?:friends|people|of us|members|pax)", lower)
    size = int(size_match.group(1)) if size_match else None
    if group_type_found or size:
        group = GroupInfo(
            type=group_type_found.capitalize() if group_type_found else None,
            size=size,
        )

    return ExtractedData(
        places=places,
        food=food,
        activities=activities,
        interests=interests,
        budget=budget,
        duration=duration,
        group=group,
    )


# ---------------------------------------------------------------------------
# Ollama-backed extractor (preferred, real LLM reasoning)
# ---------------------------------------------------------------------------

def _try_ollama_extract(text: str) -> Optional[ExtractedData]:
    payload = {
        "model": OLLAMA_MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": text,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1},
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT_SECONDS)
        resp.raise_for_status()
        raw = resp.json().get("response", "")
        data = json.loads(raw)
        group = data.get("group")
        return ExtractedData(
            places=data.get("places") or [],
            food=data.get("food") or [],
            activities=data.get("activities") or [],
            interests=data.get("interests") or [],
            budget=data.get("budget"),
            duration=data.get("duration"),
            group=GroupInfo(**group) if group else None,
        )
    except Exception:
        # Ollama not running, model not pulled, malformed JSON, timeout, etc.
        return None


# ---------------------------------------------------------------------------
# Public entrypoint used by the API layer
# ---------------------------------------------------------------------------

def extract_structured_data(text: str) -> ExtractedData:
    """
    Try the local LLM first (Ollama, CPU). If unavailable or it fails,
    fall back to the deterministic rule-based extractor so the endpoint
    always returns a usable result -- both paths are 100% offline/CPU.
    """
    llm_result = _try_ollama_extract(text)
    if llm_result is not None:
        return llm_result
    return _rule_based_extract(text)
