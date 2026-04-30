from config.connection import get_connection

def insert_categories(df, cursor):
    categories_list = df["product_category"].drop_duplicates().to_list()
    for category in categories_list:
        sql = "INSERT OR IGNORE INTO categories (name) VALUES(?)"
        cursor.execute(sql, (category,))

def insert_regions(df, cursor):
    regions_list = df["customer_region"].drop_duplicates().to_list()
    for region in regions_list:
        sql = "INSERT OR IGNORE INTO regions (name) VALUES(?)"
        cursor.execute(sql, (region,))

def switch_regions_id(df, cursor):
    sql_regions = "SELECT id, name FROM regions"
    cursor.execute(sql_regions)
    region_rows = cursor.fetchall()
    region_mapper = {row_category["name"]: row_category["id"] for row_category in region_rows}
    return df["customer_region"].map(region_mapper)

def switch_categories_id(df, cursor):
    sql_categories =  "SELECT id, name FROM categories"
    cursor.execute(sql_categories)
    categories_rows = cursor.fetchall()
    categories_mapper = {category_row["name"]: category_row["id"] for category_row in categories_rows}
    return df["product_category"].map(categories_mapper)

def insert_products(df, cursor):
    products_list = df[["product_id", "price", "product_category"]].drop_duplicates(subset="product_id").to_dict("records")
    for product in products_list:
        product_sql = "INSERT OR IGNORE INTO products (id, price, category_id) VALUES(?, ?, ?)"
        cursor.execute(product_sql, (product["product_id"], product["price"], product["product_category"]))

def insert_sales(df, cursor):
    sales_list = df.to_dict("records")
    for sale in sales_list:
        sale_sql = """
            INSERT OR IGNORE INTO sales (id, quantity_sold, rating, date, product_id, region_id)
            VALUES(?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sale_sql, (sale["order_id"], sale["quantity_sold"], sale["rating"], sale["order_date"], sale["product_id"], sale["customer_region"]))

def load_database(df):
    conn = get_connection()
    cursor = conn.cursor()

    insert_categories(df, cursor)
    insert_regions(df, cursor)
    switch_regions_id(df, cursor)
    switch_categories_id(df, cursor)
    insert_products(df, cursor)
    insert_sales(df, cursor)

    conn.commit()
    cursor.close()
    conn.close()
    