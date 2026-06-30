"""
itinerary/builder.py

Takes a list of Recommendation objects and lays them out into a simple
time-blocked day plan. Pure Python, no FastAPI/HTTP involved -- callable
directly from a Streamlit app.
"""
from datetime import datetime, timedelta
from typing import List

from chalo_backend.models.schemas import Recommendation, DayPlan, ItineraryStop

MAX_STOPS_PER_DAY = 4
BUFFER_MINUTES_BETWEEN_STOPS = 30


def build_itinerary(
    recommendations: List[Recommendation],
    start_time: str = "09:00",
    duration_days: int = 1,
) -> List[DayPlan]:
    days = []
    idx = 0

    for day_num in range(1, duration_days + 1):
        current_time = datetime.strptime(start_time, "%H:%M")
        stops = []

        for _ in range(MAX_STOPS_PER_DAY):
            if idx >= len(recommendations):
                break
            rec = recommendations[idx]
            idx += 1

            stops.append(
                ItineraryStop(
                    time=current_time.strftime("%H:%M"),
                    place=rec.name,
                    category=rec.category,
                    notes=rec.reason,
                )
            )
            duration = rec.duration_minutes or 60
            current_time += timedelta(minutes=duration + BUFFER_MINUTES_BETWEEN_STOPS)

        if stops:
            days.append(DayPlan(day=day_num, stops=stops))

        if idx >= len(recommendations):
            break

    return days
