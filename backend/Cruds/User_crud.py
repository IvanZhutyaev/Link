from sqlalchemy.orm import Session
from Models.All_models import Law_Face, User
from passlib.context import CryptContext

from Schemas.User_schema import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def create_user(db: Session, user_data: UserModel):
    if db.query(User).filter(User.Phone_number == user_data.Phone_number).first():
        raise ValueError("Пользователь с таким телефоном уже существует")

    hashed_password = hash_password(user_data.password)
    db_user = User(
        User_name=user_data.User_name,
        Phone_number=user_data.Phone_number,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_user_credentials(db: Session, phone: str, password: str) -> bool:
    # Находим usera by phone
    user = db.query(User).filter(User.Phone_number==phone).first()
    # Если не найден phone или пароль не совпадает
    if not user or not pwd_context.verify(password, user.password):
        return False

    return True



def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.Phone_number == phone).first()




def update_user(db: Session, user_id: int, user_data: UserModel):
    db_user = get_user(db, user_id)
    if not db_user:
        raise ValueError("Пользователь не найден")

    if user_data.Phone_number != db_user.Phone_number:
        if get_user_by_phone(db, user_data.Phone_number):
            raise ValueError("Номер телефона занят")

    db_user.User_name = user_data.User_name
    db_user.Phone_number = user_data.Phone_number
    if user_data.password:
        db_user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(db_user)
    return db_user


# DELETE
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise ValueError("Пользователь не найден")

    db.delete(db_user)
    db.commit()
    return {"message": "Пользователь удалён"}