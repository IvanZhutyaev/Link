from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, false, DateTime, Float, BigInteger, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.Database.DB_connection import base, engine


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
    area = Column(Integer, nullable=True)  # Площадь в м²
    rooms = Column(Integer, nullable=True)  # Количество комнат
    floor = Column(Integer, nullable=True)  # Этаж
    owner_id = Column(Integer, ForeignKey("Users.id"), nullable=True)  # Владелец квартиры
    rating = Column(Float, nullable=True, default=0.0)  # Рейтинг квартиры
    rating_count = Column(Integer, nullable=True, default=0)  # Количество оценок
    has_error = Column(BOOLEAN, nullable=False, default=False)  # Флаг ошибки
    
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


base.metadata.create_all(engine)