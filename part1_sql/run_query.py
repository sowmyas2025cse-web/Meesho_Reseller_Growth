
import sqlite3
import csv
import os

DB_PATH = os.path.join("data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join("part1sql", "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

queries = {

    # ============================================================
    # REQUIRED QUERY 1
    # Monthly revenue by category
    # ============================================================
    "monthly_category_revenue.csv": """
        SELECT
            month,
            category,
            ROUND(SUM(quantity * unit_price), 2) AS revenue,
            COUNT(*) AS n_orders
        FROM orders
        GROUP BY month, category
        ORDER BY
            CASE month
                WHEN 'April' THEN 1
                WHEN 'May' THEN 2
                WHEN 'June' THEN 3
            END,
            category;
    """,

    # ============================================================
    # REQUIRED QUERY 2
    # Region-wise total revenue and order count
    # ============================================================
    "region_revenue_orders.csv": """
        SELECT
            r.region,
            ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
            COUNT(*) AS order_count
        FROM orders o
        JOIN resellers r
            ON o.reseller_id = r.reseller_id
        GROUP BY r.region
        ORDER BY total_revenue DESC;
    """,

    # ============================================================
    # REQUIRED QUERY 3
    # Top resellers by total spend
    # HAVING total_spend > 50000
    # ============================================================
    "top_resellers_by_spend.csv": """
        SELECT
            r.reseller_id,
            r.reseller_name,
            ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
        FROM orders o
        JOIN resellers r
            ON o.reseller_id = r.reseller_id
        GROUP BY
            r.reseller_id,
            r.reseller_name
        HAVING total_spend > 50000
        ORDER BY total_spend DESC
        LIMIT 5;
    """,

    # ============================================================
    # REQUIRED QUERY 4
    # Resellers who have never placed an order
    # ============================================================
    "zero_order_resellers.csv": """
        SELECT
            r.reseller_id,
            r.reseller_name,
            r.region
        FROM resellers r
        LEFT JOIN orders o
            ON r.reseller_id = o.reseller_id
        WHERE o.order_id IS NULL;
    """,

    # ============================================================
    # REQUIRED QUERY 4B
    # Demonstrate COUNT(*) vs COUNT(order_id)
    #
    # For RS024:
    # COUNT(*) = 1
    # COUNT(order_id) = 0
    #
    # This demonstrates why COUNT(*) cannot be used to
    # identify zero-match LEFT JOIN rows.
    # ============================================================
    "zero_order_count_demo.csv": """
        SELECT
            r.reseller_id,
            r.reseller_name,
            COUNT(*) AS count_star,
            COUNT(o.order_id) AS count_order_id
        FROM resellers r
        LEFT JOIN orders o
            ON r.reseller_id = o.reseller_id
        WHERE r.reseller_id = 'RS024'
        GROUP BY
            r.reseller_id,
            r.reseller_name;
    """,

    # ============================================================
    # REQUIRED QUERY 5
    # June AOV for Delivered orders only
    # ============================================================
    "june_delivered_aov.csv": """
        SELECT
            ROUND(
                SUM(quantity * unit_price) / COUNT(*),
                2
            ) AS june_delivered_aov
        FROM orders
        WHERE month = 'June'
          AND status = 'Delivered';
    """,

    # ============================================================
    # EXTRA QUERY
    # May -> June category change
    #
    # This is useful for Part 2 and is safe to keep.
    # ============================================================
    "may_june_category_change.csv": """
        SELECT
            category,
            ROUND(
                SUM(
                    CASE
                        WHEN month = 'May'
                        THEN quantity * unit_price
                        ELSE 0
                    END
                ),
                2
            ) AS may_revenue,

            ROUND(
                SUM(
                    CASE
                        WHEN month = 'June'
                        THEN quantity * unit_price
                        ELSE 0
                    END
                ),
                2
            ) AS june_revenue,

            ROUND(
                (
                    SUM(
                        CASE
                            WHEN month = 'June'
                            THEN quantity * unit_price
                            ELSE 0
                        END
                    )
                    -
                    SUM(
                        CASE
                            WHEN month = 'May'
                            THEN quantity * unit_price
                            ELSE 0
                        END
                    )
                )
                * 100.0
                /
                SUM(
                    CASE
                        WHEN month = 'May'
                        THEN quantity * unit_price
                        ELSE 0
                    END
                ),
                2
            ) AS pct_change

        FROM orders
        WHERE month IN ('May', 'June')
        GROUP BY category
        ORDER BY category;
    """,

    # ============================================================
    # EXTRA QUERY
    # Top 5 delivered resellers
    # ============================================================
    "top5_resellers_delivered.csv": """
        SELECT
            r.reseller_id,
            r.reseller_name,
            r.region,
            ROUND(
                SUM(o.quantity * o.unit_price),
                2
            ) AS delivered_revenue,
            COUNT(*) AS delivered_orders
        FROM orders o
        JOIN resellers r
            ON o.reseller_id = r.reseller_id
        WHERE o.status = 'Delivered'
        GROUP BY
            r.reseller_id,
            r.reseller_name,
            r.region
        ORDER BY delivered_revenue DESC
        LIMIT 5;
    """,

    # ============================================================
    # EXTRA QUERY
    # Top 5 delivered resellers in May
    # ============================================================
    "may_top5_resellers.csv": """
        SELECT
            r.reseller_id,
            r.reseller_name,
            r.city,
            r.region,
            ROUND(
                SUM(o.quantity * o.unit_price),
                2
            ) AS may_delivered_revenue
        FROM orders o
        JOIN resellers r
            ON o.reseller_id = r.reseller_id
        WHERE o.month = 'May'
          AND o.status = 'Delivered'
        GROUP BY
            r.reseller_id,
            r.reseller_name,
            r.city,
            r.region
        ORDER BY may_delivered_revenue DESC
        LIMIT 5;
    """
}


for filename, query in queries.items():

    cursor.execute(query)
    rows = cursor.fetchall()

    column_names = [
        description[0]
        for description in cursor.description
    ]

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(column_names)
        writer.writerows(rows)

    print(f"{filename}: {len(rows)} rows")


conn.close()

print("\nAll Part 1 queries completed successfully.")

