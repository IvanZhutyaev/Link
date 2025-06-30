from sqlalchemy.orm import Session
from backend.Database.DB_connection import SessionLocal, engine
from backend.Models.All_models import User, Law_Face, Property, Booking, ResidentialComplex
from backend.Cruds.User_crud import create_user
from backend.Cruds.Law_crud import create_zastroy
from backend.Cruds.Property_crud import create_property
from backend.Cruds.RC_crud import create_residential_complex
from backend.Schemas.User_schema import UserModel
from backend.Schemas.Zastroy_schema import ZastroyModel
from backend.Schemas.Property_schema import PropertyModel
from backend.Schemas.RC_schema import ResidentialComplexCreate


def seed_database():
    db = SessionLocal()
    try:
        # Создаем тестовых пользователей
        test_users = [
            UserModel(
                User_name="Иван Иванов",
                Phone_number="+79991234567",
                password="password123"
            ),
            UserModel(
                User_name="Мария Петрова",
                Phone_number="+79987654321",
                password="password123"
            )
        ]
        
        created_users = []
        for user_data in test_users:
            try:
                user = create_user(db, user_data)
                created_users.append(user)
                print(f"Создан пользователь: {user.User_name}")
            except Exception as e:
                print(f"Ошибка создания пользователя: {e}")
        
        # Создаем тестовых застройщиков
        test_zastroys = [
            ZastroyModel(
                Company_name="ООО 'Солнечный Дом'",
                INN=1234567890,
                OGRN=1234567890123,
                Adress="г. Москва, ул. Солнечная, 15",
                User_name="admin_sun",
                password="password123"
            ),
            ZastroyModel(
                Company_name="ООО 'Парковый Квартал'",
                INN=9876543210,
                OGRN=9876543210987,
                Adress="г. Москва, ул. Парковая, 8",
                User_name="admin_park",
                password="password123"
            )
        ]
        
        created_zastroys = []
        for zastroy_data in test_zastroys:
            try:
                zastroy = create_zastroy(db, zastroy_data)
                created_zastroys.append(zastroy)
                print(f"Создан застройщик: {zastroy.Company_name}")
            except Exception as e:
                print(f"Ошибка создания застройщика: {e}")
        
        # Создаем тестовые жилые комплексы
        test_residential_complexes = [
            ResidentialComplexCreate(
                name="ЖК 'Солнечный'",
                address="г. Москва, ул. Солнечная, 15",
                developer_name="ООО 'Солнечный Дом'",
                zastroy_id=created_zastroys[0].id if created_zastroys else 1,
                city="Москва",
                commissioning_date="2025",
                housing_class="Комфорт",
                status="Строится",
                avatar_url="https://via.placeholder.com/300x200/007aff/ffffff?text=ЖК+Солнечный"
            ),
            ResidentialComplexCreate(
                name="ЖК 'Парковый'",
                address="г. Москва, ул. Парковая, 8",
                developer_name="ООО 'Парковый Квартал'",
                zastroy_id=created_zastroys[1].id if len(created_zastroys) > 1 else 1,
                city="Москва",
                commissioning_date="2024",
                housing_class="Эконом",
                status="Сдан",
                avatar_url="https://via.placeholder.com/300x200/34c759/ffffff?text=ЖК+Парковый"
            ),
            ResidentialComplexCreate(
                name="ЖК 'Речной'",
                address="г. Москва, наб. Речная, 12",
                developer_name="ООО 'Солнечный Дом'",
                zastroy_id=created_zastroys[0].id if created_zastroys else 1,
                city="Москва",
                commissioning_date="2026",
                housing_class="Бизнес",
                status="Планируется",
                avatar_url="https://via.placeholder.com/300x200/ff9500/ffffff?text=ЖК+Речной"
            ),
            ResidentialComplexCreate(
                name="ЖК 'Премиум'",
                address="г. Москва, ул. Премиумная, 1",
                developer_name="ООО 'Парковый Квартал'",
                zastroy_id=created_zastroys[1].id if len(created_zastroys) > 1 else 1,
                city="Москва",
                commissioning_date="2025",
                housing_class="Премиум",
                status="Строится",
                avatar_url="https://via.placeholder.com/300x200/fd7e14/ffffff?text=ЖК+Премиум"
            ),
            ResidentialComplexCreate(
                name="ЖК 'Элитный'",
                address="г. Москва, ул. Элитная, 10",
                developer_name="ООО 'Солнечный Дом'",
                zastroy_id=created_zastroys[0].id if created_zastroys else 1,
                city="Москва",
                commissioning_date="2027",
                housing_class="Элит",
                status="Планируется",
                avatar_url="https://via.placeholder.com/300x200/dc3545/ffffff?text=ЖК+Элитный"
            )
        ]
        
        created_complexes = []
        for complex_data in test_residential_complexes:
            try:
                complex_obj = create_residential_complex(db, complex_data)
                created_complexes.append(complex_obj)
                print(f"Создан жилой комплекс: {complex_obj.name}")
            except Exception as e:
                print(f"Ошибка создания жилого комплекса: {e}")
        
        # Создаем тестовую недвижимость
        test_properties = [
            PropertyModel(
                name="ЖК 'Солнечный', кв. 45",
                address="г. Москва, ул. Солнечная, 15",
                price=3200000.0,
                description="Уютная квартира с видом на парк",
                image_url="https://via.placeholder.com/300x200/007aff/ffffff?text=ЖК+Солнечный",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[0].id if created_zastroys else 1
            ),
            PropertyModel(
                name="ЖК 'Парковый', кв. 78",
                address="г. Москва, ул. Парковая, 8",
                price=4100000.0,
                description="Просторная квартира в тихом районе",
                image_url="https://via.placeholder.com/300x200/34c759/ffffff?text=ЖК+Парковый",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[1].id if len(created_zastroys) > 1 else 1
            ),
            PropertyModel(
                name="ЖК 'Речной', кв. 23",
                address="г. Москва, наб. Речная, 12",
                price=6800000.0,
                description="Элитная квартира с видом на реку",
                image_url="https://via.placeholder.com/300x200/ff9500/ffffff?text=ЖК+Речной",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[0].id if created_zastroys else 1
            ),
            PropertyModel(
                name="ЖК 'Лесной', кв. 12",
                address="г. Москва, ул. Лесная, 25",
                price=2800000.0,
                description="Компактная квартира для молодой семьи",
                image_url="https://via.placeholder.com/300x200/5856d6/ffffff?text=ЖК+Лесной",
                city="Москва",
                is_available=True,
                zastroy_id=created_zastroys[1].id if len(created_zastroys) > 1 else 1
            )
        ]
        
        created_properties = []
        for property_data in test_properties:
            try:
                property_obj = create_property(db, property_data)
                created_properties.append(property_obj)
                print(f"Создана недвижимость: {property_obj.name}")
            except Exception as e:
                print(f"Ошибка создания недвижимости: {e}")
        
        # Создаем тестовые брони
        if created_users and created_properties:
            from .Cruds.Property_crud import create_booking
            from .Schemas.Property_schema import BookingModel
            
            test_booking = BookingModel(property_id=created_properties[0].id)
            try:
                booking = create_booking(db, created_users[0].id, test_booking)
                print(f"Создана бронь для пользователя {created_users[0].User_name}")
            except Exception as e:
                print(f"Ошибка создания брони: {e}")
        
        print("База данных успешно заполнена тестовыми данными!")
        
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database() 