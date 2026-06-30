def mock_extract_response() -> dict:
    return {
        "places": ["Charminar", "Golconda Fort"],
        "food": ["Biryani"],
        "activities": ["Shopping"],
        "budget": "₹3000",
        "duration": "1 Day",
        "group": "Friends",
    }


def mock_recommendations_response() -> list[dict]:
    return [
        {
            "name": "Hotel Shadab",
            "category": "Restaurant",
            "description": "A classic stop for a hearty Hyderabad meal after your afternoon explorations.",
            "reason": "You mentioned Biryani.",
        },
        {
            "name": "Laad Bazaar",
            "category": "Shopping",
            "description": "Browse for bangles and handcrafted keepsakes near the old city core.",
            "reason": "Near Charminar.",
        },
        {
            "name": "Chowmahalla Palace",
            "category": "Historical",
            "description": "A refined historical landmark that fits your interest in heritage spots.",
            "reason": "Matches your interest in historical places.",
        },
    ]


def mock_trip_response() -> list[dict]:
    return [
        {"time": "🌅 Morning", "title": "Charminar"},
        {"time": "☕ Breakfast", "title": "Nimrah Cafe"},
        {"time": "🛍 Shopping", "title": "Laad Bazaar"},
        {"time": "🍛 Lunch", "title": "Hotel Shadab"},
        {"time": "🌇 Evening", "title": "Hussain Sagar"},
    ]
