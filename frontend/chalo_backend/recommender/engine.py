"""
recommender/engine.py

Matches structured extracted data against the local Hyderabad dataset
and returns ranked recommendations with human-readable reasons.
Pure Python, no network calls -- fully offline.
"""
from typing import List

from chalo_backend.database.hyderabad_places import PLACES
from chalo_backend.models.schemas import RecommendRequest, Recommendation


def _normalize(items: List[str]) -> List[str]:
    return [i.strip().lower() for i in items]


def get_recommendations(req: RecommendRequest, limit: int = 8) -> List[Recommendation]:
    wanted_places = _normalize(req.places)
    wanted_food = _normalize(req.food)
    wanted_activities = _normalize(req.activities)
    wanted_interests = _normalize(req.interests)

    scored = []

    for entry in PLACES:
        name_lower = entry["name"].lower()
        tags_lower = [t.lower() for t in entry["tags"]]
        near_lower = [n.lower() for n in entry["near"]]

        score = 0
        reasons = []

        # Directly named place
        if name_lower in wanted_places:
            score += 10
            reasons.append(f"You specifically mentioned {entry['name']}.")

        # Near a place the user named
        matched_near = [p for p in wanted_places if p in near_lower]
        if matched_near:
            score += 6
            nearby_name = matched_near[0].title()
            reasons.append(f"It's close to {nearby_name}, which you mentioned.")

        # Food match
        if entry["category"] == "food":
            food_matches = [f for f in wanted_food if f in tags_lower or f in name_lower]
            if food_matches:
                score += 8
                reasons.append(f"You wanted {food_matches[0].title()}, and this place is known for it.")

        # Activity match (e.g. shopping)
        activity_matches = [a for a in wanted_activities if a in tags_lower]
        if activity_matches:
            score += 5
            reasons.append(f"Matches your interest in {activity_matches[0]}.")

        # Interest match (e.g. photography, history)
        interest_matches = [i for i in wanted_interests if i in tags_lower]
        if interest_matches:
            score += 4
            reasons.append(f"You like {interest_matches[0]}, and this is a great match for that.")

        # Budget filter (soft): skip very expensive items if low budget given
        if req.budget is not None and entry["avg_cost"] > req.budget:
            score -= 3

        if score > 0:
            scored.append((score, entry, reasons))

    # Sort by score, descending
    scored.sort(key=lambda x: x[0], reverse=True)

    recommendations = []
    for score, entry, reasons in scored[:limit]:
        recommendations.append(
            Recommendation(
                name=entry["name"],
                category=entry["category"],
                reason=" ".join(reasons) if reasons else "Popular spot in Hyderabad.",
                lat=entry["lat"],
                lng=entry["lng"],
                avg_cost=entry["avg_cost"],
                duration_minutes=entry["duration_minutes"],
            )
        )

    # Fallback: if nothing matched at all (e.g. empty extraction), suggest top picks
    if not recommendations:
        defaults = ["Charminar", "Laad Bazaar", "Hotel Shadab", "Golconda Fort"]
        for entry in PLACES:
            if entry["name"] in defaults:
                recommendations.append(
                    Recommendation(
                        name=entry["name"],
                        category=entry["category"],
                        reason="Popular must-visit spot in Hyderabad.",
                        lat=entry["lat"],
                        lng=entry["lng"],
                        avg_cost=entry["avg_cost"],
                        duration_minutes=entry["duration_minutes"],
                    )
                )

    return recommendations
