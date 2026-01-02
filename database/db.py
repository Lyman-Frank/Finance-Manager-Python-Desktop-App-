# подключение к SQLite

import sqlite3
from pathlib import Path

# путь к базе данных
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "finance.db"


def get_connection():
    """
    Возвращает соединение с SQLite БД
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # чтобы получать данные как словарь
    return conn


def init_db():
    """
    Создаёт таблицы и индексы, если их нет
    """
    conn = get_connection()
    cursor = conn.cursor()

    # таблица категорий
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    """)

    # таблица транзакций
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
        amount REAL NOT NULL CHECK(amount > 0),
        category_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        comment TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    """)

    # индексы
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_transactions_date
    ON transactions(date);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_transactions_type
    ON transactions(type);
    """)

    # базовые категории
    cursor.executemany("""
    INSERT OR IGNORE INTO categories (name)
    VALUES (?);
    """, [
        ("Еда",),
        ("Транспорт",),
        ("Развлечения",),
        ("Зарплата",),
        ("Другое",)
    ])

    conn.commit()
    conn.close()
