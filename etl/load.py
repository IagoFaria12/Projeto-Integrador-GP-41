from config.connection import get_connection

def insert_categories(df, cursor):
    categories = df["product_category"].drop_duplicates().to_list()
    for category in categories:
        sql = "INSERT OR IGNORE INTO categories (name) VALUES(?)"
        cursor.execute(sql, (category,))

def insert_regions(df, cursor):
    regions = df["customer_region"].drop_duplicates().to_list()
    for region in regions:
        sql = "INSERT OR IGNORE INTO regions (name) VALUES(?)"
        cursor.execute(sql, (region,))

def switch_regions_id(df, cursor):
    sql = "SELECT id, name FROM regions"
    cursor.execute(sql)
    rows = cursor.fetchall()
    mapper = {row_category["name"]: row_category["id"] for row_category in rows}
    df["customer_region"] = df["customer_region"].map(mapper)
    return df

def switch_categories_id(df, cursor):
    sql =  "SELECT id, name FROM categories"
    cursor.execute(sql)
    rows = cursor.fetchall()
    mapper = {category_row["name"]: category_row["id"] for category_row in rows}
    df["product_category"] = df["product_category"].map(mapper)

    return df

def insert_products(df, cursor):
    products = df[["product_id", "price", "product_category"]].drop_duplicates(subset="product_id").to_dict("records")
    for product in products:
        sql = "INSERT OR IGNORE INTO products (id, price, category_id) VALUES(?, ?, ?)"
        cursor.execute(sql, (product["product_id"], product["price"], product["product_category"]))

def insert_sales(df, cursor):
    sales = df.to_dict("records")
    for sale in sales:
        sql = """
            INSERT OR IGNORE INTO sales (id, quantity_sold, discount_percent, rating, date, product_id, region_id)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (sale["order_id"], sale["quantity_sold"], sale["discount_percent"], sale["rating"], sale["order_date"], sale["product_id"], sale["customer_region"]))

def load_database(df):
    conn, cursor = get_connection()

    insert_categories(df, cursor)
    insert_regions(df, cursor)
    df = switch_regions_id(df, cursor)
    df = switch_categories_id(df, cursor)
    insert_products(df, cursor)
    insert_sales(df, cursor)

    conn.commit()
    cursor.close()
    conn.close()
    