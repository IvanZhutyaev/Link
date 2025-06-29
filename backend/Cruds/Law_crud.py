from sqlalchemy.orm import Session
from backend.Models.All_models import Law_Face
from passlib.context import CryptContext

from backend.Schemas.Zastroy_schema import ZastroyModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# CREATE
def create_zastroy(db: Session, zastroy_data: ZastroyModel):
    # Проверка на уникальность ИНН/ОГРН
    if db.query(Law_Face).filter(Law_Face.INN == zastroy_data.INN).first():
        raise ValueError("Застройщик с таким ИНН уже существует")
    if db.query(Law_Face).filter(Law_Face.OGRN == zastroy_data.OGRN).first():
        raise ValueError("Застройщик с таким ОГРН уже существует")

    hashed_password = hash_password(zastroy_data.password)
    db_zastroy = Law_Face(
        **zastroy_data.model_dump(exclude={"password"}),
        password=hashed_password
    )
    db.add(db_zastroy)
    db.commit()
    db.refresh(db_zastroy)
    return db_zastroy


def check_zastroy_credentials(db: Session, inn: int, password: str) -> bool:
    # Находим застройщика по ИНН
    zastroy = db.query(Law_Face).filter(Law_Face.INN == inn).first()

    # Если не найден или пароль не совпадает
    if not zastroy or not pwd_context.verify(password, zastroy.password):
        return False

    return True


# READ
def get_zastroy(db: Session, zastroy_id: int):
    return db.query(Law_Face).filter(Law_Face.id == zastroy_id).first()


def get_zastroys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Law_Face).offset(skip).limit(limit).all()


def get_zastroy_by_inn(db: Session, inn: int):
    return db.query(Law_Face).filter(Law_Face.INN == inn).first()


# UPDATE
def update_zastroy(db: Session, zastroy_id: int, zastroy_data: ZastroyModel):
    db_zastroy = get_zastroy(db, zastroy_id)
    if not db_zastroy:
        raise ValueError("Застройщик не найден")

    # Обновляем данные (кроме пароля)
    update_data = zastroy_data.model_dump(exclude_unset=True, exclude={"password"})
    for key, value in update_data.items():
        setattr(db_zastroy, key, value)

    # Обновляем пароль, если он передан
    if zastroy_data.password:
        db_zastroy.password = hash_password(zastroy_data.password)

    db.commit()
    db.refresh(db_zastroy)
    return db_zastroy


# DELETE
def delete_zastroy(db: Session, zastroy_id: int):
    db_zastroy = get_zastroy(db, zastroy_id)
    if not db_zastroy:
        raise ValueError("Застройщик не найден")

    db.delete(db_zastroy)
    db.commit()
    return {"message": "Застройщик удалён"}

