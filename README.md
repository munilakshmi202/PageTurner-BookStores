<<<<<<< HEAD
# PageTurner BookStore — Complete Project

The Python Flask + SQLite backend is in `PageTurner_BookStore/`. Open `PageTurner_BookStore/app.py` for the application entry point.

1. Back up the `.db` files.
2. Open `PageTurner_BookStore/` in VS Code.
3. Run `py -m pip install -r requirements.txt`.
4. Run `py app.py`.
5. Run tests with `py -m unittest discover -s tests -v`.

The `demo/` directory is the supplied React/Vite practice project. The advanced bookstore steps and test instructions are documented in `PageTurner_BookStore/README.md`.


## Admin access and testing

- Start the Flask app from `PageTurner_BookStore/` with `python app.py` after installing `requirements.txt`.
- On a fresh database, the initial administrator password is `admin123`. Change it before using this app outside local development.
- Open `/admin/login`, sign in with the administrator password, and use **Admin Dashboard** to access the store dashboard, analytics, reports, user management, order management, and CSV export.
- Run tests from the Flask app directory with `python -m unittest discover -s tests -v`.
=======
# PageTurner Books

PageTurner Books is an online bookstore application developed using
Python Flask, SQLite, HTML, CSS and JavaScript.

## Technologies Used

Python

Flask

SQLite

HTML

CSS

JavaScript


## Main Features

1. View available books

2. Search books by title and author

3. Filter books by category

4. Sort books by title and price

5. Pagination with 6 books per page

6. View book details

7. View stock availability

8. Add books to cart

9. Update cart quantity

10. Remove books from cart

11. Checkout and place orders

12. Automatically reduce stock after purchase

13. Prevent purchasing more books than available stock

14. Add ratings and reviews

15. Find previous orders using phone number

16. Admin login

17. Admin book management

18. Add books

19. Edit books

20. Delete books

21. View admin sales reports

22. Responsive design for desktop and mobile


## Project Structure

PageTurner_BookStore

    app.py

    schema.sql

    seed.sql

    bookstore.db

    queries.sql

    README.md

    templates

        base.html

        home.html

        book.html

        cart.html

        checkout.html

        order.html

        find_order.html

        admin_login.html

        admin.html

        admin_book_form.html

        admin_reports.html

        404.html

    static

        style.css

        script.js


## Database

The project uses SQLite as the database.

The database file is:

bookstore.db

The main database tables are:

books

orders

order_items

reviews


## Books Table

The books table stores:

Book ID

Title

Author

Category

Price

Description

Stock

Cover Color


## Orders Table

The orders table stores:

Order ID

Customer Name

Phone

Address

Total

Order Date


## Order Items Table

The order_items table stores:

Order ID

Book ID

Quantity

Price


## Reviews Table

The reviews table stores:

Book ID

Customer Name

Rating

Comment

Created Date


## Stock Management

Stock is checked before adding a book to the cart.

Stock is checked again during checkout.

When an order is successfully placed, the purchased quantity is
removed from the available stock.

The application prevents the stock from becoming negative.

The checkout process uses a database transaction so that stock
updates remain safe when multiple customers try to purchase books.


## Reviews and Ratings

Customers can submit a rating from 1 to 5.

Customers can also submit a review comment.

The book page displays the average rating and number of reviews.

The average rating is calculated using the SQL AVG function.


## Admin Area

The admin area is protected using a session.

The admin password is defined once in app.py using the
ADMIN_PASSWORD variable.

The password is not stored in the database.

The admin can:

Add books

Edit books

Delete books

View store reports

Logout


## Admin Reports

The admin report provides:

Total orders

Total revenue

Total books sold

Best selling books

Orders per category

Books sold per category

Revenue per category

SQL aggregate functions such as COUNT, SUM and GROUP BY are used
for reporting.


## Running the Project

Open the PageTurner_BookStore folder in VS Code.

Open the VS Code terminal.

Run:

python app.py

If python does not work on the system, try:

py app.py


## Open the Website

After Flask starts successfully, open the local address shown in
the terminal.

Usually it is:

http://127.0.0.1:5000


## Database Testing

The SQLite database can be opened using a SQLite database viewer.

The following tables can be checked:

books

orders

order_items

reviews


## Testing Stock

Place an order for a book.

Check the books table.

The stock value should decrease by the purchased quantity.

When the stock becomes zero, the website should display:

Out of Stock


## Testing Reviews

Open a book details page.

Submit two different ratings.

The average rating should be calculated from the submitted ratings.


## Testing Order History

Place an order using a phone number.

Open Find My Order.

Enter the same phone number.

The previous order should be displayed.


## Testing Admin

Open the Admin page.

Enter the admin password.

After successful login, the admin dashboard should be displayed.

Without login, the admin dashboard should redirect to the
admin login page.


## SQL Query File

The queries.sql file contains 8 required SQL queries.

The queries include:

Category filtering

Book searching

Order searching

Out of stock books

Low stock books

Total orders and revenue

Best selling books

Orders per category


## Security Practices

SQL values are passed using parameterized queries with ? placeholders.

Database changes use commit.

Database transactions are used during checkout.

Admin access is protected using a session.

The application checks stock before completing an order.


## Project Completion

The PageTurner Books project demonstrates a complete online
bookstore workflow using Flask, SQLite, HTML, CSS and JavaScript.
>>>>>>> 1ae86f74bb1d3078f76d9a3b07b0114531db70d0
