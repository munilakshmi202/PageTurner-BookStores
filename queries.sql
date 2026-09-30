-- 1. All books cheaper than 500
SELECT *
FROM books
WHERE price < 500
ORDER BY price;

-- 2. Technology books sorted by price, highest first
SELECT *
FROM books
WHERE category = 'Technology'
ORDER BY price DESC;

-- 3. Number of books in each category
SELECT category, COUNT(*) AS book_count
FROM books
GROUP BY category
ORDER BY category;

-- 4. The most expensive book
SELECT *
FROM books
ORDER BY price DESC
LIMIT 1;

-- 5. Each order with the customer name and total
SELECT id, customer_name, total, created_at
FROM orders
ORDER BY id DESC;
