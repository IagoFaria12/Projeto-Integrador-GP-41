from config.connection import get_connection

def sales_by_category():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT c.name AS category, SUM(s.quantity_sold) AS quantity
        FROM sales AS s
        INNER JOIN products AS p
        ON s.product_id = p.id
        INNER JOIN categories AS c
        ON p.category_id = c.id
        GROUP BY p.category_id
    """
    rows = cursor.execute(sql)
    return rows

def discount_comparison():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT
            CASE
                WHEN s.discount_percent > 0 THEN "with_discount"
                ELSE "without_discount"
            END AS category_discount,
            SUM(s.quantity_sold) AS sales_total
        FROM sales AS s
        GROUP BY category_discount
    """

    rows = cursor.execute(sql)
    return rows

def average_order():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT SUM(s.quantity_sold) / COUNT(*) AS average_order
        FROM sales AS s
    """

    rows = cursor.execute(sql)
    return rows

def top_sold():
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT c.name AS category, p.price, SUM(s.quantity_sold) AS quantity_sold
        FROM sales AS s
        INNER JOIN products AS p
        ON s.product_id = p.id
        INNER JOIN categories AS c
        ON p.category_id = c.id
        GROUP BY s.product_id
        ORDER BY quantity_sold DESC
        LIMIT 5
    """
    rows = cursor.execute(sql)
    return rows

