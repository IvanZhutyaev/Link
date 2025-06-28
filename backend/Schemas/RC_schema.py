from typing import Optional
from pydantic import BaseModel, Field


class ResidentialComplexCreate(BaseModel):
    name: str                      # Название (обязательное)
    address: str                   # Адрес (обязательное)
    developer_name: str            # Имя застройщика (обязательное)
    zastroy_id: int                # ID застройщика (обязательное)
    city: str                      # Город (обязательное)
    commissioning_date: Optional[str] = None  # Ввод в эксплуатацию (необязательное)
    housing_class: Optional[str] = None        # Класс (необязательное)
    status: Optional[str] = None               # Статус (необязательное)
    avatar_url: Optional[str] = None           # Ссылка на аватар (необязательное)
    
    class Config:
        from_attributes = True  # Работает с ORM (для FastAPI >= 2.0)


class ResidentialComplexResponse(ResidentialComplexCreate):
    id: int
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    
    class Config:
        from_attributes = True


class RatingModel(BaseModel):
    rating: float = Field(ge=1.0, le=5.0, description="Рейтинг от 1 до 5")