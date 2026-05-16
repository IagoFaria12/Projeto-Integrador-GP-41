from config.connection import get_connection
from utils.filters import filter_year_month

# KPI Items per Order
def items_per_order(categories = None, current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT ROUND(AVG(quantity_sold), 2) AS items_per_order
    FROM sales AS s
    """

    params, sql = filter_year_month(sql, categories, current_year, first_month, last_month)
    cursor.execute(sql, (params))

    row = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return row

# Lines Chart Sales Evolution Over Time
def order_evolution_over_time(categories = None, current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT s.date ,COUNT(s.id) as order_total
    FROM sales as s
    INNER JOIN products AS p ON s.product_id = p.id
    """

    params, sql = filter_year_month(sql, categories, current_year, first_month, last_month)

    sql += """
    GROUP BY s.date
    ORDER BY order_total DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def gross_evolution_over_time(categories = None, current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT s.date, ROUND(SUM(p.price * s.quantity_sold), 2) AS gross_total
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    """

    params, sql = filter_year_month(sql, categories, current_year, first_month, last_month)

    sql += """
    GROUP BY s.date
    ORDER BY gross_total DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

# Bars Chart Sales by Region
def order_by_region(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT r.name AS region, COUNT(s.id) AS sales_total 
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    INNER JOIN regions as r ON s.region_id = r.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql += """
    GROUP BY r.id
    ORDER BY sales_total DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return rows

def gross_by_region(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT r.name, ROUND(SUM(p.price * s.quantity_sold), 2) AS gross_total
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    INNER JOIN regions AS r ON s.region_id = r.id
    """
    params, sql = filter_year_month(current_year, first_month, last_month)
    
    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    sql += """
    GROUP BY r.id
    ORDER BY sales_total DESC
    """

    cursor.close()
    conn.close()

    return rows

# Table Top Selling Products
def order_top_sales(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT s.product_id, c.name AS category, ROUND(p.price, 2) as price, ROUND(AVG(s.rating), 1) AS average_rating, SUM(s.quantity_sold) AS quantity_sold
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
    LIMIT 10
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

# Pie Chart Sales by Category   
def order_by_category(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT c.name, COUNT(s.id) as sales_total
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    INNER JOIN categories AS c ON p.category_id = c.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql +=  """
    GROUP BY c.id
    ORDER BY sales_total DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def gross_by_category(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT c.name, ROUND(SUM(p.price * s.quantity_sold), 2) AS gross_total
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    INNER JOIN categories as c ON p.category_id = c.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql += """
    GROUP BY c.id
    ORDER BY gross_total DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

# Pie Chart Discount vs Non-Discount Sales
def order_discount_comparison(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT
        CASE
            WHEN s.discount_percent > 0 THEN "with_discount"
            ELSE "without_discount"
        END AS category_discount,
    COUNT(s.id) AS order_total
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)
    
    sql += """
    GROUP BY category_discount
    """

    rows = cursor.execute(sql, params)

    cursor.close()
    conn.close()

    return rows

def gross_discount_comparison(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT
        CASE
            WHEN s.discount_percent > 0 THEN "with_discount"
            ELSE "without_discount"
        END AS category_discount,
    ROUND(SUM(p.price * s.quantity_sold),2) AS gross_total
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql += """
    GROUP BY category_discount
    ORDER BY gross_total DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

# Bars Chart Price Range Distribution
def order_price_range_distribution(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT COUNT(s.id) AS order_total,
        CASE
            WHEN p.price > 100.00 AND p.price < 200.00 THEN "Mid"
            WHEN P.PRICE > 200.00 AND p.price < 500.00 THEN "High"
            ELSE "Low"
    END AS price_range
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql += """
    GROUP BY price_range
    ORDER BY order_total DESC
    """
     
    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def gross_price_range_distribution(current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT ROUND(SUM(p.price * s.quantity_sold) ,2) AS gross_total,
        CASE
            WHEN p.price > 100.00 AND p.price < 200.00 THEN "Mid"
            WHEN p.price > 200.00 AND p.price < 500.00 THEN "High"
            ELSE "Low"
        END AS price_range
    FROM sales AS s
    INNER JOIN products AS p ON s.product_id = p.id
    """

    params, sql = filter_year_month(sql, current_year, first_month, last_month)

    sql += """
    GROUP BY price_range
    ORDER BY gross_total DESC
    """

    cursor.execute(sql, (params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def gross_total_revenue(categories = None, current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT 
         ROUND(SUM(p.price * s.quantity_sold),2 ) AS total_gross_revenue
    FROM sales s
    INNER JOIN products p
    ON s.product_id = p.id
    """

    params, sql = filter_year_month(sql,categories, current_year, first_month, last_month)

    cursor.execute(sql, (params))
    rows = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return rows

def total_revenue_with_discount(categories = None, current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT 
    ROUND(SUM((p.price - (p.price * s.discount_percent / 100.0)) * s.quantity_sold),2) AS total_revenue
    FROM sales s
    INNER JOIN products p
    ON s.product_id = p.id

    """

    params, sql = filter_year_month(sql,categories, current_year, first_month, last_month)

    cursor.execute(sql, (params))
    rows = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return rows

def total_number_of_orders(categories = None, current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT 
    COUNT(s.id) AS quantity_total_orders
    FROM sales s;

    """

    params, sql = filter_year_month(sql,categories, current_year, first_month, last_month)

    cursor.execute(sql, (params))
    rows = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return rows

def average_evaluation_of_products(categories = None, current_year = None, first_month = None, last_month = None):

    conn, cursor = get_connection()

    sql = """
    SELECT
    ROUND((SUM(s.rating)) / COUNT(s.rating), 1) AS average_product_evaluation
    FROM sales AS s 

    """

    params, sql = filter_year_month(sql,categories, current_year, first_month, last_month)

    cursor.execute(sql, (params))
    rows = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return rows

def avarege_tickets(categories=None, current_year=None, first_month=None, last_month=None):

    conn, cursor = get_connection()

    sql = """
    WITH ticket_average AS (
        SELECT 
            p.price,
            s.quantity_sold,
            s.discount_percent,

            ROUND(
                (p.price - (p.price * s.discount_percent / 100.0)) 
                * s.quantity_sold,
                2
            ) AS total_order_revenue

        FROM sales AS s

        INNER JOIN products AS p
            ON s.product_id = p.id
    ),

    grupos AS (
        SELECT
            total_order_revenue,

            NTILE(3) OVER (
                ORDER BY total_order_revenue
            ) AS ticket_group

        FROM ticket_average
    ),

    categorized_sales AS (
        SELECT 
            total_order_revenue,

            CASE 
                WHEN ticket_group = 1 THEN 'low cost'
                WHEN ticket_group = 2 THEN 'medium cost'
                ELSE 'high cost'
            END AS category

        FROM grupos
    )

    SELECT 
        category,
        COUNT(*) AS quantity_orders,

        ROUND(
            AVG(total_order_revenue),
            2
        ) AS average_ticket

    FROM categorized_sales
    """

    # params, sql = filter_year_month(
    #     sql,
    #     categories,
    #     current_year,
    #     first_month,
    #     last_month
    # )

    sql += """
    GROUP BY category
    ORDER BY average_ticket ASC;
    """

    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows