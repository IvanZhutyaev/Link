import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from environs import Env

env=Env()
env.read_env()
db_path=env.str('database_path')
print(f"Подключение к базе данных: {db_path}")
engine = create_engine(db_path)
SessionLocal=sessionmaker(bind=engine, autocommit=False, autoflush=False)

base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Создает все таблицы в базе данных"""
    try:
        print("Попытка создания таблиц...")
        base.metadata.create_all(engine)
        print("Таблицы успешно созданы")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        print(f"Тип ошибки: {type(e)}")
        # Не прерываем работу приложения, если не удалось создать таблицы
