from Database.DB_connection import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE residential_complexes ADD COLUMN avaline_url VARCHAR;"))
    conn.commit()
    print("Столбец avaline_url успешно добавлен!") 