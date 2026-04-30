import pandas as pd
from config.connection import get_connection

def load_database():

    conn = get_connection()
    cursor = conn.cursor()

    df =  pd.read_csv("data/processed/amazon_sales_dataset.csv")

    categories_list = df["product_category"].drop_duplicates().to_list()

    for category in categories_list:
        sql = "INSERT OR IGNORE INTO categories (name) VALUES(?)"
        cursor.execute(sql, (category,))

    regions_list = df["customer_region"].drop_duplicates().to_list()

    for region in regions_list:
        sql = "INSERT OR IGNORE INTO regions (name) VALUES(?)"
        cursor.execute(sql, (region,))

    sql_categories = "SELECT id, name FROM regions"
    cursor.execute(sql_categories)
    region_rows = cursor.fetchall()

    region_mapper = {row_category["name"]: row_category["id"] for row_category in region_rows}

    df["customer_region"] = df["customer_region"].map(region_mapper)




        

    
    
