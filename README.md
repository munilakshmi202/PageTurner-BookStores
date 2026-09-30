# PageTurner Books — Online Book Store

A beginner-friendly online bookstore built with:

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Jinja templates

## 1. Requirements

Install Python 3.10 or newer.

Flask is the only external Python package used.

## 2. Install Flask

Open a terminal in this project folder:

```bash
python -m pip install flask
```

On Windows, if `python` does not work, try:

```bash
py -m pip install flask
```

## 3. Run the project

```bash
python app.py
```

Then open:

http://127.0.0.1:5000

On first startup, Flask creates `bookstore.db`, creates the three tables and inserts the sample books.

## 4. Project structure

```text
PageTurner_BookStore/
│
├── app.py
├── schema.sql
├── seed.sql
├── queries.sql
├── README.md
├── bookstore.db          # created automatically after first run
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── book.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order.html
│   └── 404.html
│
└── static/
    ├── style.css
    └── script.js
```

## 5. Routes

| Route | Purpose | SQL |
|---|---|---|
| `/` | Show books and category filter | SELECT books |
| `/book/<id>` | Show book details | SELECT by id |
| `/cart/add/<id>` | Add one copy to cart | SELECT book; session update |
| `/cart` | Show cart and total | SELECT books by IDs |
| `/cart/update/<id>` | Change quantity | SELECT stock; session update |
| `/cart/remove/<id>` | Remove a cart item | Session update |
| `/checkout` | Show checkout and create order | INSERT orders, INSERT order_items, UPDATE books |
| `/order/<id>` | Show confirmation | SELECT order + JOIN order_items/books |

## 6. Important project concepts

### Cart

The cart is stored in Flask's session:

```text
{
    "1": 2,
    "5": 1
}
```

The keys are strings because session data is serialized. When querying SQLite, the IDs are converted back to integers.

### Order saving

Checkout performs these operations:

1. Validate customer details.
2. Recheck stock.
3. INSERT into `orders`.
4. Get the new order ID using `lastrowid`.
5. INSERT each product into `order_items`.
6. Reduce stock.
7. Commit the transaction.
8. Clear the session cart.
9. Redirect to the confirmation page.

### SQL safety

SQL values are passed with `?` placeholders. This avoids directly inserting user input into SQL statements.

## 7. JavaScript features

- Live title/author search
- Remove confirmation
- Exactly 10 digit phone validation
- Green success messages disappear after 3 seconds
- Mobile navigation menu

## 8. Test checklist

1. Open home page.
2. Search for a title or author.
3. Click a category.
4. Open a book.
5. Add a book to cart.
6. Increase/decrease quantity.
7. Try quantity `0`.
8. Remove a book and confirm the browser prompt.
9. Go to checkout.
10. Submit blank fields.
11. Submit an invalid phone number.
12. Submit a valid 10-digit phone number.
13. Confirm the order.
14. Open `bookstore.db` with SQLite tools and check `orders` and `order_items`.

## 9. Reset the database

Stop Flask, delete `bookstore.db`, then run:

```bash
python app.py
```

The database will be recreated from `schema.sql` and `seed.sql`.

## 10. 5-minute demo flow

- Start the Flask application.
- Show the home page and responsive book cards.
- Demonstrate category filtering.
- Demonstrate live search.
- Open a book detail page.
- Add the book to cart.
- Change quantity and show the total.
- Go to checkout.
- Show validation for an incorrect phone number.
- Place a valid order.
- Show the confirmation page.
- Explain that `orders` stores customer/order information and `order_items` stores each book belonging to the order.
