-- ==========================================
-- PAGETURNER BOOK STORE
-- REQUIRED SQL QUERIES
-- ==========================================


-- 1. Find books by category
SELECT *
FROM books
WHERE category = ?;


-- 2. Search books by title or author
SELECT *
FROM books
WHERE title LIKE ?
   OR author LIKE ?;


-- 3. Find an order using customer phone number
SELECT
    o.id AS order_id,
    o.customer_name,
    o.phone,
    o.address,
    o.total,
    o.created_at,
    b.title,
    oi.quantity,
    oi.price
FROM orders o
JOIN order_items oi
    ON o.id = oi.order_id
JOIN books b
    ON oi.book_id = b.id
WHERE o.phone = ?
ORDER BY o.created_at DESC;


-- 4. Find books that are currently out of stock
SELECT *
FROM books
WHERE stock = 0;


-- 5. Find books with low stock
SELECT *
FROM books
WHERE stock > 0
  AND stock <= ?;


-- 6. Total orders and total revenue
SELECT
    COUNT(*) AS total_orders,
    COALESCE(SUM(total), 0) AS total_revenue
FROM orders;


-- 7. Best selling books
SELECT
    b.id,
    b.title,
    b.author,
    b.category,
    SUM(oi.quantity) AS quantity_sold,
    SUM(oi.quantity * oi.price) AS revenue
FROM order_items oi
JOIN books b
    ON oi.book_id = b.id
GROUP BY
    b.id,
    b.title,
    b.author,
    b.category
ORDER BY quantity_sold DESC;


-- 8. Orders and sales grouped by category
SELECT
    b.category,
    COUNT(DISTINCT oi.order_id) AS order_count,
    SUM(oi.quantity) AS quantity_sold,
    SUM(oi.quantity * oi.price) AS revenue
FROM order_items oi
JOIN books b
    ON oi.book_id = b.id
GROUP BY b.category
ORDER BY revenue DESC;
