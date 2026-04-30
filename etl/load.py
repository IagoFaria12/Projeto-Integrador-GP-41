from config.connection import get_connection

def load_database(df):

    conn = get_connection()
    cursor = conn.cursor()

    categories_list = df["product_category"].drop_duplicates().to_list()
    for category in categories_list:
        sql = "INSERT OR IGNORE INTO categories (name) VALUES(?)"
        cursor.execute(sql, (category,))

    regions_list = df["customer_region"].drop_duplicates().to_list()
    for region in regions_list:
        sql = "INSERT OR IGNORE INTO regions (name) VALUES(?)"
        cursor.execute(sql, (region,))

    products_list = df[["product_id", "price"]].drop_duplicates(subset="product_id").to_dict("records")
    for product in products_list:
        product_sql = "INSERT OR IGNORE INTO products (id, price) VALUES(?, ?)"
        cursor.execute(product_sql, (product["product_id"], product["price"]))

    sql_regions = "SELECT id, name FROM regions"
    cursor.execute(sql_regions)
    region_rows = cursor.fetchall()
    region_mapper = {row_category["name"]: row_category["id"] for row_category in region_rows}
    df["customer_region"] = df["customer_region"].map(region_mapper)

    sql_categories =  "SELECT id, name FROM categories"
    cursor.execute(sql_categories)
    categories_rows = cursor.fetchall()
    categories_mapper = {category_row["name"]: category_row["id"] for category_row in categories_rows}
    df["product_category"] = df["product_category"].map(categories_mapper)

    sales_list = df.to_dict("records")
    for sale in sales_list:
        sale_sql = """
            INSERT OR IGNORE INTO sales (id, quantity_sold, rating, date, category_id, product_id, region_id)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sale_sql, (sale["order_id"], sale["quantity_sold"], sale["rating"], sale["order_date"], sale["product_category"], sale["product_id"], sale["customer_region"]))


    conn.commit()
    






        

    
    
