"""
Shared Pydantic schemas for requests and responses.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


# ---------- /extract ----------

class ExtractRequest(BaseModel):
    text: str = Field(..., description="Raw unstructured text: blog, guide, or user query")


class GroupInfo(BaseModel):
    type: Optional[str] = None   # "Friends", "Family", "Couple", "Solo"
    size: Optional[int] = None


class ExtractedData(BaseModel):
    places: List[str] = []
    food: List[str] = []
    activities: List[str] = []
    interests: List[str] = []
    budget: Optional[int] = None
    duration: Optional[str] = None
    group: Optional[GroupInfo] = None


# ---------- /recommend ----------

class RecommendRequest(BaseModel):
    places: List[str] = []
    food: List[str] = []
    activities: List[str] = []
    interests: List[str] = []
    budget: Optional[int] = None
    duration: Optional[str] = None
    group: Optional[GroupInfo] = None


class Recommendation(BaseModel):
    name: str
    category: str
    reason: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    avg_cost: Optional[int] = None
    duration_minutes: Optional[int] = None


class RecommendResponse(BaseModel):
    recommendations: List[Recommendation]


# ---------- /itinerary ----------

class ItineraryRequest(BaseModel):
    recommendations: List[Recommendation]
    start_time: Optional[str] = "09:00"
    duration_days: Optional[int] = 1


class ItineraryStop(BaseModel):
    time: str
    place: str
    category: str
    notes: Optional[str] = None


class DayPlan(BaseModel):
    day: int
    stops: List[ItineraryStop]


class ItineraryResponse(BaseModel):
    trip: List[DayPlan]


# ---------- /upload ----------

class UploadResponse(BaseModel):
    filename: str
    extracted_text: str
    char_count: int
