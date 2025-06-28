from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PropertyModel(BaseModel):
    name: str = Field(max_length=100)
    address: str = Field(max_length=255)
    price: int = Field(gt=0)
    description: Optional[str] = None
    image_url: Optional[str] = None
    city: str = Field(max_length=100)
    is_available: bool = True
    zastroy_id: int
    complex_id: Optional[int] = None
    area: Optional[int] = None  # Площадь в м²
    rooms: Optional[int] = None  # Количество комнат
    floor: Optional[int] = None  # Этаж


class PropertyResponse(PropertyModel):
    id: int
    area: Optional[int] = None
    rooms: Optional[int] = None
    floor: Optional[int] = None
    owner_id: Optional[int] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    has_error: bool = False

    class Config:
        from_attributes = True


class PropertySearch(BaseModel):
    city: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    rooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    is_available: Optional[bool] = True
    complex_id: Optional[int] = None  # Поиск по ЖК


class RatingModel(BaseModel):
    rating: float = Field(ge=1.0, le=5.0, description="Рейтинг от 1 до 5")


class BookingModel(BaseModel):
    property_id: int


class BookingResponse(BaseModel):
    id: int
    user_id: int
    property_id: int
    booking_date: datetime
    status: str
    expires_at: Optional[datetime] = None
    property: PropertyResponse

    class Config:
        from_attributes = True


class PurchaseModel(BaseModel):
    property_id: int
    purchase_price: int = Field(gt=0)
    payment_method: str = Field(..., description="cash, mortgage, installment")
    booking_id: Optional[int] = None


class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    property_id: int
    purchase_date: datetime
    purchase_price: int
    payment_method: str
    status: str
    booking_id: Optional[int] = None
    property: PropertyResponse

    class Config:
        from_attributes = True


class MortgageModel(BaseModel):
    property_id: int
    loan_amount: int = Field(gt=0)
    down_payment: int = Field(gt=0)
    interest_rate: float = Field(gt=0, le=100)
    loan_term_years: int = Field(gt=0, le=30)
    bank_name: Optional[str] = None
    application_notes: Optional[str] = None
    booking_id: Optional[int] = None


class MortgageResponse(BaseModel):
    id: int
    user_id: int
    property_id: int
    application_date: datetime
    loan_amount: int
    down_payment: int
    interest_rate: float
    loan_term_years: int
    monthly_payment: float
    status: str
    bank_name: Optional[str] = None
    application_notes: Optional[str] = None
    approved_date: Optional[datetime] = None
    booking_id: Optional[int] = None
    property: PropertyResponse

    class Config:
        from_attributes = True


class MortgageCalculationModel(BaseModel):
    property_price: int = Field(gt=0)
    down_payment_percent: float = Field(gt=0, le=100)
    interest_rate: float = Field(gt=0, le=100)
    loan_term_years: int = Field(gt=0, le=30)


class MortgageCalculationResponse(BaseModel):
    loan_amount: int
    down_payment: int
    monthly_payment: float
    total_payment: float
    total_interest: float 