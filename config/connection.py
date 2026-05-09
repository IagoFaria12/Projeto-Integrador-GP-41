import sqlite3

def get_connection():
    conn = sqlite3.connect("data/amazon_sales.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor