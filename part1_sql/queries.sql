-- QUERY 1
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


-- QUERY 2
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS delivered_revenue,
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
-- QUERY 3
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
-- QUERY 4
SELECT
    category,
    ROUND(SUM(CASE WHEN month = 'May'
                   THEN quantity * unit_price ELSE 0 END), 2) AS may_revenue,
    ROUND(SUM(CASE WHEN month = 'June'
                   THEN quantity * unit_price ELSE 0 END), 2) AS june_revenue,
    ROUND(
        (
            SUM(CASE WHEN month = 'June'
                     THEN quantity * unit_price ELSE 0 END)
            -
            SUM(CASE WHEN month = 'May'
                     THEN quantity * unit_price ELSE 0 END)
        )
        * 100.0
        /
        SUM(CASE WHEN month = 'May'
                 THEN quantity * unit_price ELSE 0 END),
        2
    ) AS pct_change
FROM orders
WHERE month IN ('May', 'June')
GROUP BY category
ORDER BY category;
-- QUERY 5
SELECT
    r.reseller_id,
    r.reseller_name,
    r.city,
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS may_delivered_revenue
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