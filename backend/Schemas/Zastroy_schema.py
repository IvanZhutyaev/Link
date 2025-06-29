from pydantic import BaseModel, Field
from typing import Optional
from .DeveloperRating_schema import DeveloperRatingResponse


class ZastroyModel(BaseModel):
    Company_name : str = Field(max_length=50)
    INN: int  = Field()
    OGRN: int  = Field()
    Adress: str = Field(max_length=255)
    User_name: str = Field(max_length=255)
    password:str=Field(max_length=255)


class ZastroyResponse(ZastroyModel):
    id: int
    rating: Optional[DeveloperRatingResponse] = None

    class Config:
        from_attributes = True


class ZastroyLogin(BaseModel):
    inn: int
    password: str


class ZastroyWithStatsResponse(ZastroyModel):
    id: int
    rating: Optional[DeveloperRatingResponse] = None
    stats: Optional[dict] = None  # Статистика застройщика
    
    class Config:
        from_attributes = True


