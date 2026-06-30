from __future__ import annotations

from typing import Any


def is_page_available(page: str, hero_completed: bool, recommendations_unlocked: bool, planner_unlocked: bool) -> bool:
    if page == "hero":
        return True
    if page == "dashboard":
        return hero_completed
    if page == "extractor":
        return hero_completed
    if page == "recommendations":
        return recommendations_unlocked
    if page == "planner":
        return planner_unlocked
    return False


def get_page_title(page: str) -> str:
    titles = {
        "hero": "Hero",
        "dashboard": "Dashboard",
        "extractor": "AI Extractor",
        "recommendations": "Recommendations",
        "planner": "Trip Planner",
    }
    return titles.get(page, "Dashboard")
