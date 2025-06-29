from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, false, DateTime, Float, BigInteger, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import random
from sqlalchemy.ext.declarative import declarative_base
from Database.DB_connection import base, engine


class Law_Face(base):
    __tablename__="Law_faces"
    id = Column(Integer,primary_key=True, index=True)
    Company_name = Column(String, nullable=False)
    INN=Column(Integer, unique=True)
    OGRN=Column(Integer, unique=True)
    Adress=Column(String, nullable=False)
    User_name=Column(String, nullable=False)
    password=Column(String, nullable=False)
    IsVerified=Column(BOOLEAN, nullable=False, default=True)
    
    # Связи
    properties = relationship("Property", back_populates="zastroy")
    residential_complexes = relationship("ResidentialComplex", back_populates="zastroy")
    rating = relationship("DeveloperRating", back_populates="law_face", uselist=False, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Автоматическое создание рейтинга при инициализации
        self.create_developer_rating()

    def create_developer_rating(self):
        """Автоматически создает рейтинг для застройщика"""
        if not self.rating:
            rating_data = self.calculate_initial_rating()
            self.rating = DeveloperRating(
                law_face_id=self.id,
                rating=rating_data["rating"],
                completed_projects=rating_data["completed_projects"],
                years_on_market=rating_data["years_on_market"]
            )

    def calculate_initial_rating(self):
        """Генерация тестовых данных и расчет рейтинга"""
        random.seed(self.INN)  # Для детерминированных результатов

        completed_projects = (self.INN % 20) + random.randint(1, 10)
        years_on_market = (self.INN % 25) + 5

        rating = min(
            8.0 + (completed_projects * 0.3) + (years_on_market * 0.2),
            10.0
        )

        return {
            "rating": round(rating, 1),
            "completed_projects": completed_projects,
            "years_on_market": years_on_market
        }


class User(base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    User_name=Column(String, nullable=False, default="undified")
    Phone_number=Column(String, nullable=False, default="undified")
    Email=Column(String, nullable=False, default="undified")
    password=Column(String, nullable=False, default="undified")
    IsVerified=Column(BOOLEAN, nullable=False, default=True)
    
    # Связи
    bookings = relationship("Booking", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
    mortgages = relationship("Mortgage", back_populates="user")


class Property(base):
    __tablename__ = "Properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    city = Column(String, nullable=False)
    is_available = Column(BOOLEAN, nullable=False, default=True)
    zastroy_id = Column(Integer, ForeignKey("Law_faces.id"), nullable=False)
    complex_id = Column(Integer, ForeignKey("residential_complexes.id"), nullable=True)  # ЖК
    area = Column(Float, nullable=True)  # Площадь в м² (может быть дробной)
    rooms = Column(Integer, nullable=True)  # Количество комнат
    floor = Column(Integer, nullable=True)  # Этаж
    owner_id = Column(Integer, ForeignKey("Users.id"), nullable=True)  # Владелец квартиры
    rating = Column(Float, nullable=True, default=0.0)  # Рейтинг квартиры
    rating_count = Column(Integer, nullable=True, default=0)  # Количество оценок
    has_error = Column(BOOLEAN, nullable=False, default=False)  # Флаг ошибки
    status = Column(String, nullable=False, default="available")  # Статус квартиры (available, sold, reserved)
    
    # Связи
    zastroy = relationship("Law_Face", back_populates="properties")
    complex = relationship("ResidentialComplex", back_populates="properties")
    events = relationship("ApartmentEvent", back_populates="property")
    bookings = relationship("Booking", back_populates="property")
    purchases = relationship("Purchase", back_populates="property")
    mortgages = relationship("Mortgage", back_populates="property")


class Booking(base):
    __tablename__ = "Bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("Properties.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default="booked")  # booked, cancelled, expired, converted_to_purchase
    expires_at = Column(DateTime, nullable=True)  # Дата истечения брони
    
    # Связи
    user = relationship("User", back_populates="bookings")
    property = relationship("Property", back_populates="bookings")


class Purchase(base):
    __tablename__ = "Purchases"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("Properties.id"), nullable=False)
    purchase_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    purchase_price = Column(BigInteger, nullable=False)  # Фактическая цена покупки
    payment_method = Column(String, nullable=False)  # cash, mortgage, installment
    status = Column(String, nullable=False, default="completed")  # pending, completed, cancelled
    booking_id = Column(Integer, ForeignKey("Bookings.id"), nullable=True)  # Связь с бронированием
    
    # Связи
    user = relationship("User", back_populates="purchases")
    property = relationship("Property", back_populates="purchases")


class Mortgage(base):
    __tablename__ = "Mortgages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("Properties.id"), nullable=False)
    application_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    loan_amount = Column(BigInteger, nullable=False)  # Сумма кредита
    down_payment = Column(BigInteger, nullable=False)  # Первоначальный взнос
    interest_rate = Column(Float, nullable=False)  # Процентная ставка
    loan_term_years = Column(Integer, nullable=False)  # Срок кредита в годах
    monthly_payment = Column(Float, nullable=False)  # Ежемесячный платеж
    status = Column(String, nullable=False, default="pending")  # pending, approved, rejected, active, closed
    bank_name = Column(String, nullable=True)  # Название банка
    application_notes = Column(Text, nullable=True)  # Примечания к заявке
    approved_date = Column(DateTime, nullable=True)  # Дата одобрения
    booking_id = Column(Integer, ForeignKey("Bookings.id"), nullable=True)  # Связь с бронированием
    
    # Связи
    user = relationship("User", back_populates="mortgages")
    property = relationship("Property", back_populates="mortgages")


class ResidentialComplex(base):
    __tablename__ = "residential_complexes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)              # Название
    address = Column(String, nullable=False)          # Адрес
    developer_name = Column(String, nullable=False)   # Имя застройщика
    zastroy_id = Column(Integer, ForeignKey("Law_faces.id"), nullable=False)  # ID застройщика
    city = Column(String, nullable=False)             # Город
    commissioning_date = Column(String, nullable=False)                 # Ввод в эксплуатацию (может быть NULL)
    housing_class = Column(String)                    # Класс (эконом, комфорт, бизнес)
    status = Column(String)                           # Статус дома (строится, сдан, планируется)
    avatar_url = Column(String)                       # Ссылка на аватар
    avaline_url = Column(String)                      # Ссылка на 3D-тур AvaLine
    rating = Column(Float, nullable=True, default=0.0)  # Рейтинг ЖК
    rating_count = Column(Integer, nullable=True, default=0)  # Количество оценок
    
    # Связи
    zastroy = relationship("Law_Face", back_populates="residential_complexes")
    properties = relationship("Property", back_populates="complex")


class ApartmentEvent(base):
    __tablename__ = "apartment_events"
    
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("Properties.id"), nullable=False)
    user_id = Column(String(255), nullable=False)  # Обычная строка для ID пользователя
    event_type = Column(String(100), nullable=False)  # Тип события (click_3d_tour, click_book, time_on_page, etc.)
    event_value = Column(Float, nullable=True)  # Значение события (например, время на странице)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Связь с объектом недвижимости
    property = relationship("Property", back_populates="events")


class DeveloperRating(base):
    __tablename__ = "developer_ratings"

    id = Column(Integer, primary_key=True, index=True)
    law_face_id = Column(Integer, ForeignKey("Law_faces.id"), unique=True)
    rating = Column(Float, default=0.0)  # 0-10 (рассчитывается)
    completed_projects = Column(Integer, default=0)  # Сданные объекты (из API ФНС)
    years_on_market = Column(Integer, default=0)  # Стаж компании (лет)
    last_updated = Column(DateTime, default=datetime.utcnow)

    law_face = relationship("Law_Face", back_populates="rating")


base.metadata.create_all(engine)