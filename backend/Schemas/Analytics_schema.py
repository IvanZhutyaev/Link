from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    apartment_id: int
    user_id: str
    event_type: str
    event_value: Optional[float] = None

class EventResponse(BaseModel):
    id: int
    apartment_id: int
    user_id: str
    event_type: str
    event_value: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnalyticsSummary(BaseModel):
    total_events: int
    unique_users: int
    events_by_type: dict
    average_time_on_page: Optional[float] = None
    most_viewed_apartments: list 