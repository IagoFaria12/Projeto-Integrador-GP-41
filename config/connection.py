import sqlite3

def get_connection():
    conn = sqlite3.connect("data/amazon_sales.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def init_database():
    conn, cursor = get_connection()

    with open("config/schema.sql", "r", encoding="utf-8") as file:
        cursor.executescript(file.read())
        conn.close()