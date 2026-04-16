"""
Простой ETL-скрипт: читает Excel с лидами, чистит телефоны,
удаляет дубли, загружает в PostgreSQL.
"""

import pandas as pd
import psycopg2
import re
from psycopg2.extras import execute_values

def clean_phone(phone):
    """Оставляет только цифры, убирает код страны если есть +7 или 8."""
    if not isinstance(phone, str):
        return None
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('7') and len(digits) == 11:
        digits = digits[1:]  # убираем 7
    elif digits.startswith('8') and len(digits) == 11:
        digits = digits[1:]
    elif len(digits) == 10:
        pass
    else:
        return None
    return digits

def main():
    # 1. Extract
    df = pd.read_excel('leads_export.xlsx', sheet_name='Лиды')
    
    # 2. Transform
    df['phone_clean'] = df['phone'].apply(clean_phone)
    df = df.dropna(subset=['phone_clean'])
    df = df.drop_duplicates(subset=['phone_clean'])
    df['created_at'] = pd.Timestamp.now()
    
    # 3. Load
    conn = psycopg2.connect(
        host="localhost",
        database="crm_db",
        user="analyst",
        password="******"  # в реальности бери из переменных окружения
    )
    cur = conn.cursor()
    
    # Создаём таблицу, если нет
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
            name TEXT,
            phone TEXT UNIQUE,
            created_at TIMESTAMP
        )
    """)
    
    # Вставляем пачкой
    data = list(zip(df['name'], df['phone_clean'], df['created_at']))
    execute_values(cur, 
                   "INSERT INTO leads (name, phone, created_at) VALUES %s ON CONFLICT (phone) DO NOTHING",
                   data)
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Загружено {len(data)} уникальных лидов")

if __name__ == "__main__":
    main()
