from Database.DB_connection import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='residential_complexes'
    """))
    print("Столбцы в residential_complexes:")
    for row in result:
        print(row[0]) 