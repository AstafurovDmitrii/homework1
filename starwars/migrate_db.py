import sqlite3
from pathlib import Path

DB_NAME = "starwars_characters.db"

def migrate_database():
    Path("data").mkdir(exist_ok=True)  # Создаёт папку `data`, если её нет
    
    with sqlite3.connect(f"data/{DB_NAME}") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birth_year TEXT,
            eye_color TEXT,
            films TEXT,
            gender TEXT,
            hair_color TEXT,
            height TEXT,
            homeworld TEXT,
            mass TEXT,
            skin_color TEXT,
            species TEXT,
            starships TEXT,
            vehicles TEXT,
            created TEXT,
            edited TEXT
        )
        """)
        print("✅ База данных создана!")

if __name__ == "__main__":
    migrate_database()