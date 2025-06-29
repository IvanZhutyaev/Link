from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DeveloperRatingBase(BaseModel):
    rating: float = Field(ge=0.0, le=10.0, description="Рейтинг от 0 до 10")
    completed_projects: int = Field(ge=0, description="Количество завершенных проектов")
    years_on_market: int = Field(ge=0, description="Количество лет на рынке")


class DeveloperRatingCreate(DeveloperRatingBase):
    law_face_id: int


class DeveloperRatingUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0.0, le=10.0, description="Рейтинг от 0 до 10")
    completed_projects: Optional[int] = Field(None, ge=0, description="Количество завершенных проектов")
    years_on_market: Optional[int] = Field(None, ge=0, description="Количество лет на рынке")


class DeveloperRatingResponse(DeveloperRatingBase):
    id: int
    law_face_id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True


class DeveloperStatsResponse(BaseModel):
    properties_count: int
    complexes_count: int
    avg_property_rating: float
    avg_complex_rating: float
    overall_rating: float
    
    class Config:
        from_attributes = True


class TopDeveloperResponse(BaseModel):
    id: int
    company_name: str
    rating: float
    completed_projects: int
    years_on_market: int
    
    class Config:
        from_attributes = True 