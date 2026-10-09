-- Business reporting queries on the loaded SQLite database
SELECT COUNT(*) AS orders, ROUND(SUM(line_total), 2) AS revenue FROM sales;

SELECT product, SUM(quantity) AS units_sold,
       ROUND(SUM(line_total), 2) AS revenue
FROM sales GROUP BY product ORDER BY revenue DESC;

SELECT SUBSTR(order_date, 1, 7) AS sales_month,
       COUNT(*) AS orders, ROUND(SUM(line_total), 2) AS revenue
FROM sales GROUP BY sales_month ORDER BY sales_month;

SELECT customer_id, COUNT(*) AS orders,
       ROUND(SUM(line_total), 2) AS revenue
FROM sales GROUP BY customer_id ORDER BY revenue DESC;
