from config.connection import get_connection
from utils.query_filters import filter_year_month

def sales_by_category(current_year = None, first_month = None, last_month = None):
    
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT c.name AS category, SUM(s.quantity_sold) AS quantity
    FROM sales AS s
    INNER JOIN products AS p
    ON s.product_id = p.id
    INNER JOIN categories AS c
    ON p.category_id = c.id	
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql +=  """
    GROUP BY c.id
    ORDER BY quantity DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()
    return rows


def discount_comparison(current_year = None, first_month = None, last_month = None):
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
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)
    
    sql += """
    GROUP BY category_discount
    """

    rows = cursor.execute(sql, params)
    return rows

def average_order(current_year = None, first_month = None, last_month = None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT SUM(s.quantity_sold) / COUNT(*) AS average_order
    FROM sales AS s
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    rows = cursor.execute(sql, params)
    return rows

def top_sold(current_year = None, first_month = None, last_month = None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT s.product_id, c.name AS category, p.price, SUM(s.quantity_sold) AS quantity_sold
    FROM sales AS s
    INNER JOIN products AS p
    ON s.product_id = p.id
    INNER JOIN categories AS c
    ON p.category_id = c.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql += """
    GROUP BY s.product_id
    ORDER BY quantity_sold DESC
    LIMIT 5
    """

    rows = cursor.execute(sql, params)
    return rows

