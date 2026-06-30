"""
chalo_backend/__init__.py

Convenience re-exports so the Streamlit frontend (app.py) can do:

    from chalo_backend import extract_structured_data, get_recommendations, build_itinerary

instead of importing from each submodule individually.

NOTE: this bypasses FastAPI/HTTP entirely -- everything here is a plain
Python function call, which is what Streamlit Cloud needs since it runs
a single script, not a web server with routes.
"""
from chalo_backend.extractor.ai_extractor import extract_structured_data
from chalo_backend.recommender.engine import get_recommendations
from chalo_backend.itinerary.builder import build_itinerary

__all__ = [
    "extract_structured_data",
    "get_recommendations",
    "build_itinerary",
]
