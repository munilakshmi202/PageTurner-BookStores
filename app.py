from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort
)

import sqlite3
import os
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

app.secret_key = "pageturner-secret-key-2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "pageturner.db")


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            author TEXT NOT NULL,

            category TEXT NOT NULL,

            price REAL NOT NULL DEFAULT 0,

            description TEXT,

            stock INTEGER NOT NULL DEFAULT 10,

            cover_color TEXT,

            image TEXT

        )
    """)

    columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(books)"
        ).fetchall()
    ]

    if "image" not in columns:

        conn.execute(
            "ALTER TABLE books ADD COLUMN image TEXT"
        )

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password_hash TEXT NOT NULL

        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS admins (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            password_hash TEXT NOT NULL

        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_name TEXT NOT NULL,

            phone TEXT NOT NULL,

            address TEXT NOT NULL,

            user_id INTEGER,

            total REAL NOT NULL DEFAULT 0,

            discount REAL NOT NULL DEFAULT 0,

            created_at TEXT NOT NULL,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE SET NULL

        )
    """)

    order_columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(orders)"
        ).fetchall()
    ]

    if "discount" not in order_columns:

        conn.execute("""
            ALTER TABLE orders
            ADD COLUMN discount REAL NOT NULL DEFAULT 0
        """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS order_items (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            order_id INTEGER NOT NULL,

            book_id INTEGER NOT NULL,

            quantity INTEGER NOT NULL CHECK(quantity > 0),

            price REAL NOT NULL CHECK(price >= 0),

            FOREIGN KEY (order_id)
                REFERENCES orders(id)
                ON DELETE CASCADE,

            FOREIGN KEY (book_id)
                REFERENCES books(id)
                ON DELETE RESTRICT

        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            book_id INTEGER NOT NULL,

            name TEXT NOT NULL,

            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),

            comment TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (book_id)
                REFERENCES books(id)
                ON DELETE CASCADE

        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            book_id INTEGER NOT NULL,

            UNIQUE(user_id, book_id),

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (book_id)
                REFERENCES books(id)
                ON DELETE CASCADE

        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS coupons (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code TEXT NOT NULL UNIQUE,

            percent REAL NOT NULL,

            expiry_date TEXT NOT NULL,

            active INTEGER NOT NULL DEFAULT 1

        )
    """)

    books = [

        (
            "The Silent Patient",
            "Alex Michaelides",
            "Fiction",
            449,
            "A psychological thriller about a woman who stops speaking after a shocking crime.",
            8,
            "#7c3aed",
            "https://covers.openlibrary.org/b/isbn/9781250301697-M.jpg"
        ),

        (
            "The Alchemist",
            "Paulo Coelho",
            "Fiction",
            299,
            "A philosophical story about following dreams and discovering one's purpose.",
            12,
            "#ea580c",
            "https://covers.openlibrary.org/b/isbn/9780062315007-M.jpg"
        ),

        (
            "The Midnight Library",
            "Matt Haig",
            "Fiction",
            399,
            "A story about choices, possibilities and the lives we could have lived.",
            10,
            "#2563eb",
            "https://covers.openlibrary.org/b/isbn/9780525559474-M.jpg"
        ),

        (
            "Clean Code",
            "Robert C. Martin",
            "Technology",
            799,
            "A practical guide to writing clean, readable and maintainable software.",
            7,
            "#0f766e",
            "https://covers.openlibrary.org/b/isbn/9780132350884-M.jpg"
        ),

        (
            "Python Crash Course",
            "Eric Matthes",
            "Technology",
            699,
            "A hands-on introduction to programming with Python.",
            9,
            "#16a34a",
            "https://covers.openlibrary.org/b/isbn/9781593279288-M.jpg"
        ),

        (
            "Head First Java",
            "Kathy Sierra",
            "Technology",
            899,
            "An easy-to-understand introduction to Java programming.",
            6,
            "#dc2626",
            "https://covers.openlibrary.org/b/isbn/9781491910771-M.jpg"
        ),

        (
            "Atomic Habits",
            "James Clear",
            "Self-Help",
            499,
            "A practical guide to building good habits and breaking bad ones.",
            15,
            "#0891b2",
            "https://covers.openlibrary.org/b/isbn/9780735211292-M.jpg"
        ),

        (
            "The 7 Habits of Highly Effective People",
            "Stephen R. Covey",
            "Self-Help",
            399,
            "Principles for personal effectiveness and professional growth.",
            11,
            "#ca8a04",
            "https://covers.openlibrary.org/b/isbn/9781982137274-M.jpg"
        ),

        (
            "Think Like a Monk",
            "Jay Shetty",
            "Self-Help",
            349,
            "Lessons for finding purpose, peace and a meaningful life.",
            10,
            "#9333ea",
            "https://covers.openlibrary.org/b/isbn/9781982134488-M.jpg"
        ),

        (
            "A Brief History of Time",
            "Stephen Hawking",
            "Science",
            599,
            "An accessible exploration of the universe, time and modern physics.",
            8,
            "#1d4ed8",
            "https://covers.openlibrary.org/b/isbn/9780553380163-M.jpg"
        ),

        (
            "Cosmos",
            "Carl Sagan",
            "Science",
            549,
            "A journey through science, space, history and humanity.",
            9,
            "#4338ca",
            "https://covers.openlibrary.org/b/isbn/9780349107035-M.jpg"
        ),

        (
            "Sapiens",
            "Yuval Noah Harari",
            "History",
            649,
            "A broad history of humankind from early humans to modern society.",
            13,
            "#b45309",
            "https://covers.openlibrary.org/b/isbn/9780062316097-M.jpg"
        ),

        (
            "The Silk Roads",
            "Peter Frankopan",
            "History",
            749,
            "A history of the world through the ancient trading routes.",
            5,
            "#be123c",
            "https://covers.openlibrary.org/b/isbn/9781101912379-M.jpg"
        ),

        (
            "India After Gandhi",
            "Ramachandra Guha",
            "History",
            699,
            "A detailed history of India after independence.",
            6,
            "#15803d",
            "https://covers.openlibrary.org/b/isbn/9780060958589-M.jpg"
        )
    ]

    for book in books:

        existing = conn.execute("""
            SELECT id
            FROM books
            WHERE title = ?
        """, (book[0],)).fetchone()

        if existing:

            conn.execute("""
                UPDATE books
                SET image = ?
                WHERE id = ?
            """, (
                book[7],
                existing["id"]
            ))

        else:

            conn.execute("""
                INSERT INTO books
                (
                    title,
                    author,
                    category,
                    price,
                    description,
                    stock,
                    cover_color,
                    image
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, book)

    admin_exists = conn.execute("""
        SELECT id
        FROM admins
        LIMIT 1
    """).fetchone()

    if admin_exists is None:

        conn.execute("""
            INSERT INTO admins
            (password_hash)
            VALUES (?)
        """, (
            generate_password_hash("admin123"),
        ))

    default_coupons = [
        ("SAVE10", 10, "2099-12-31"),
        ("SAVE20", 20, "2099-12-31"),
        ("WELCOME15", 15, "2099-12-31")
    ]

    for code, percent, expiry in default_coupons:

        coupon_exists = conn.execute("""
            SELECT id
            FROM coupons
            WHERE code = ?
        """, (code,)).fetchone()

        if coupon_exists is None:

            conn.execute("""
                INSERT INTO coupons
                (code, percent, expiry_date, active)
                VALUES (?, ?, ?, 1)
            """, (
                code,
                percent,
                expiry
            ))

    conn.commit()
    conn.close()


# ============================================================
# CART COUNT
# ============================================================

@app.context_processor
def inject_cart_count():

    cart = session.get("cart", {})

    count = 0

    for quantity in cart.values():

        try:
            count += int(quantity)

        except:
            pass

    return {
        "cart_count": count
    }

# ============================================================
# LOGIN REQUIRED DECORATOR
# ============================================================

def login_required(function):

    @wraps(function)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login to continue.",
                "error"
            )

            return redirect(
                url_for(
                    "login",
                    next=request.path
                )
            )

        return function(*args, **kwargs)

    return wrapped_view
# ============================================================
# ADMIN REQUIRED
# ============================================================

def admin_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if not session.get("admin_logged_in"):

            return redirect(
                url_for("admin_login")
            )

        return view(*args, **kwargs)

    return wrapped_view


# ============================================================
# HOME
# ============================================================

@app.route("/")
@login_required
def home():

    search = request.args.get(
        "search",
        ""
    ).strip()

    category = request.args.get(
        "category",
        ""
    ).strip()

    conn = get_db()

    query = """
        SELECT *
        FROM books
        WHERE 1 = 1
    """

    params = []

    if search:

        query += """
            AND (
                title LIKE ?
                OR author LIKE ?
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value
        ])

    if category:

        query += """
            AND category = ?
        """

        params.append(category)

    query += """
        ORDER BY id ASC
    """

    books = conn.execute(
        query,
        params
    ).fetchall()

    categories = conn.execute("""
        SELECT DISTINCT category
        FROM books
        ORDER BY category
    """).fetchall()

    conn.close()

    return render_template(
        "home.html",
        books=books,
        categories=categories,
        search=search,
        selected_category=category
    )
# ============================================================
# BOOK DETAIL
# ============================================================

@app.route("/book/<int:book_id>")
def book_detail(book_id):

    conn = get_db()

    book = conn.execute("""
        SELECT
            b.*,
            COALESCE(AVG(r.rating), 0) AS average_rating,
            COUNT(r.id) AS review_count
        FROM books b
        LEFT JOIN reviews r
            ON b.id = r.book_id
        WHERE b.id = ?
        GROUP BY b.id
    """, (book_id,)).fetchone()

    reviews = conn.execute("""
        SELECT *
        FROM reviews
        WHERE book_id = ?
        ORDER BY id DESC
    """, (book_id,)).fetchall()

    conn.close()

    if book is None:

        flash(
            "Book not found.",
            "error"
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "book.html",
        book=book,
        reviews=reviews
    )


# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not name or not email or not password:

            flash(
                "All fields are required.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        conn = get_db()

        existing = conn.execute("""
            SELECT id
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        if existing:

            conn.close()

            flash(
                "Email already registered.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        password_hash = generate_password_hash(
            password
        )

        conn.execute("""
            INSERT INTO users
            (name, email, password_hash)
            VALUES (?, ?, ?)
        """, (
            name,
            email,
            password_hash
        ))

        conn.commit()
        conn.close()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password_hash"],
            password
        ):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            flash(
                "Login successful.",
                "success"
            )

            next_page = request.args.get("next")

            if next_page:
                return redirect(next_page)

            return redirect(
                url_for("home")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("user_email", None)

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# ADD TO CART
# ============================================================

@app.route(
    "/add-to-cart/<int:book_id>",
    methods=["POST"]
)
def add_to_cart(book_id):

    conn = get_db()

    book = conn.execute("""
        SELECT *
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    conn.close()

    if book is None:

        flash(
            "Book not found.",
            "error"
        )

        return redirect(
            url_for("home")
        )

    if book["stock"] <= 0:

        flash(
            "Book is out of stock.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("home")
        )

    cart = session.get(
        "cart",
        {}
    )

    key = str(book_id)

    current_quantity = int(
        cart.get(key, 0)
    )

    if current_quantity >= book["stock"]:

        flash(
            "You cannot add more than available stock.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("home")
        )

    cart[key] = current_quantity + 1

    session["cart"] = cart
    session.modified = True

    flash(
        f"{book['title']} added to cart.",
        "success"
    )

    return redirect(
        request.referrer or
        url_for("home")
    )


# ============================================================
# CART
# ============================================================

@app.route("/cart")
def cart():

    cart_data = session.get(
        "cart",
        {}
    )

    conn = get_db()

    items = []
    subtotal = 0

    for book_id, quantity in cart_data.items():

        try:

            book_id_int = int(book_id)
            quantity_int = int(quantity)

        except:

            continue

        book = conn.execute("""
            SELECT *
            FROM books
            WHERE id = ?
        """, (book_id_int,)).fetchone()

        if book:

            item_total = (
                book["price"] *
                quantity_int
            )

            items.append({
                "book": book,
                "quantity": quantity_int,
                "item_total": item_total,
                "subtotal": item_total
            })

            subtotal += item_total

    conn.close()

    discount_percent = session.get(
        "coupon_percent",
        0
    )

    coupon_code = session.get(
        "coupon_code"
    )

    discount_amount = (
        subtotal *
        discount_percent /
        100
    )

    total = subtotal - discount_amount

    return render_template(
        "cart.html",
        items=items,
        subtotal=subtotal,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        total=total,
        coupon_code=coupon_code
    )


# ============================================================
# UPDATE CART
# ============================================================

@app.route(
    "/update-cart/<int:book_id>",
    methods=["POST"]
)
def update_cart(book_id):

    quantity = request.form.get(
        "quantity",
        "1"
    )

    try:

        quantity = int(quantity)

    except:

        quantity = 1

    cart = session.get(
        "cart",
        {}
    )

    key = str(book_id)

    if key not in cart:

        return redirect(
            url_for("cart")
        )

    conn = get_db()

    book = conn.execute("""
        SELECT *
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    conn.close()

    if book is None:

        cart.pop(key, None)

        session["cart"] = cart
        session.modified = True

        flash(
            "Book not found.",
            "error"
        )

        return redirect(
            url_for("cart")
        )

    if quantity <= 0:

        cart.pop(key, None)

        session["cart"] = cart
        session.modified = True

        flash(
            "Book removed from cart.",
            "success"
        )

        return redirect(
            url_for("cart")
        )

    if quantity > book["stock"]:

        flash(
            f"Only {book['stock']} copies are available.",
            "error"
        )

        return redirect(
            url_for("cart")
        )

    cart[key] = quantity

    session["cart"] = cart
    session.modified = True

    flash(
        "Cart updated successfully.",
        "success"
    )

    return redirect(
        url_for("cart")
    )


# ============================================================
# REMOVE FROM CART
# ============================================================

@app.route(
    "/remove-from-cart/<int:book_id>",
    methods=["POST"]
)
def remove_from_cart(book_id):

    cart = session.get(
        "cart",
        {}
    )

    key = str(book_id)

    if key in cart:

        cart.pop(key)

        session["cart"] = cart
        session.modified = True

        flash(
            "Book removed from cart.",
            "success"
        )

    return redirect(
        url_for("cart")
    )


# ============================================================
# APPLY COUPON
# ============================================================

@app.route(
    "/apply-coupon",
    methods=["POST"]
)
def apply_coupon():

    code = request.form.get(
        "coupon_code",
        ""
    ).strip().upper()

    if not code:

        flash(
            "Please enter a coupon code.",
            "error"
        )

        return redirect(
            url_for("cart")
        )

    conn = get_db()

    coupon = conn.execute("""
        SELECT *
        FROM coupons
        WHERE code = ?
        AND active = 1
    """, (code,)).fetchone()

    conn.close()

    if coupon is None:

        flash(
            "Invalid or inactive coupon.",
            "error"
        )

        return redirect(
            url_for("cart")
        )

    try:

        expiry = datetime.strptime(
            coupon["expiry_date"],
            "%Y-%m-%d"
        ).date()

        if expiry < datetime.now().date():

            flash(
                "Coupon has expired.",
                "error"
            )

            return redirect(
                url_for("cart")
            )

    except ValueError:

        flash(
            "Invalid coupon expiry date.",
            "error"
        )

        return redirect(
            url_for("cart")
        )

    session["coupon_code"] = coupon["code"]
    session["coupon_percent"] = coupon["percent"]

    session.modified = True

    flash(
        f"Coupon {coupon['code']} applied successfully.",
        "success"
    )

    return redirect(
        url_for("cart")
    )


# ============================================================
# REMOVE COUPON
# ============================================================

@app.route(
    "/remove-coupon",
    methods=["POST"]
)
def remove_coupon():

    session.pop(
        "coupon_code",
        None
    )

    session.pop(
        "coupon_percent",
        None
    )

    session.modified = True

    flash(
        "Coupon removed.",
        "success"
    )

    return redirect(
        url_for("cart")
    )


# ============================================================
# CHECKOUT
# ============================================================

@app.route(
    "/checkout",
    methods=["GET", "POST"]
)
def checkout():

    cart_data = session.get(
        "cart",
        {}
    )

    if not cart_data:

        flash(
            "Your cart is empty.",
            "error"
        )

        return redirect(
            url_for("cart")
        )

    conn = get_db()

    items = []
    subtotal = 0

    for book_id, quantity in cart_data.items():

        try:

            book_id_int = int(book_id)
            quantity_int = int(quantity)

        except:

            continue

        if quantity_int <= 0:
            continue

        book = conn.execute("""
            SELECT *
            FROM books
            WHERE id = ?
        """, (book_id_int,)).fetchone()

        if book is None:
            continue

        if quantity_int > book["stock"]:

            conn.close()

            flash(
                f"Only {book['stock']} copies of {book['title']} are available.",
                "error"
            )

            return redirect(
                url_for("cart")
            )

        item_total = (
            book["price"] *
            quantity_int
        )

        # FIXED: subtotal added for checkout template
        items.append({
            "book": book,
            "quantity": quantity_int,
            "item_total": item_total,
            "subtotal": item_total
        })

        subtotal += item_total

    discount_percent = session.get(
        "coupon_percent",
        0
    )

    coupon_code = session.get(
        "coupon_code"
    )

    discount_amount = (
        subtotal *
        discount_percent /
        100
    )

    total = subtotal - discount_amount

    if request.method == "POST":

        customer_name = request.form.get(
            "customer_name",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        if (
            not customer_name
            or not phone
            or not address
        ):

            conn.close()

            flash(
                "All checkout fields are required.",
                "error"
            )

            return redirect(
                url_for("checkout")
            )

        user_id = session.get(
            "user_id"
        )

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor = conn.execute("""
            INSERT INTO orders
            (
                customer_name,
                phone,
                address,
                user_id,
                total,
                discount,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            phone,
            address,
            user_id,
            total,
            discount_amount,
            created_at
        ))

        order_id = cursor.lastrowid

        for item in items:

            book = item["book"]
            quantity = item["quantity"]

            conn.execute("""
                INSERT INTO order_items
                (
                    order_id,
                    book_id,
                    quantity,
                    price
                )
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                book["id"],
                quantity,
                book["price"]
            ))

            conn.execute("""
                UPDATE books
                SET stock = stock - ?
                WHERE id = ?
            """, (
                quantity,
                book["id"]
            ))

        conn.commit()
        conn.close()

        session["cart"] = {}

        session.pop(
            "coupon_code",
            None
        )

        session.pop(
            "coupon_percent",
            None
        )

        session.modified = True

        return redirect(
            url_for(
                "order_success",
                order_id=order_id
            )
        )

    conn.close()

    return render_template(
        "checkout.html",
        items=items,
        subtotal=subtotal,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        total=total,
        coupon_code=coupon_code
    )
# ============================================================
# ORDER SUCCESS
# ============================================================

@app.route(
    "/order-success/<int:order_id>"
)
def order_success(order_id):

    conn = get_db()

    order = conn.execute("""
        SELECT *
        FROM orders
        WHERE id = ?
    """, (order_id,)).fetchone()

    items = conn.execute("""
        SELECT
            oi.*,
            b.title,
            b.author,
            b.image
        FROM order_items oi
        JOIN books b
            ON oi.book_id = b.id
        WHERE oi.order_id = ?
    """, (order_id,)).fetchall()

    conn.close()

    if order is None:

        abort(404)

    return render_template(
        "orders_success.html",
        order=order,
        items=items
    )


# ============================================================
# FIND MY ORDER
# ============================================================

@app.route(
    "/find-order",
    methods=["GET", "POST"]
)
def find_order():

    orders = None
    searched_phone = ""

    if request.method == "POST":

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        searched_phone = phone

        phone_digits = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        if len(phone_digits) >= 10:

            phone_digits = phone_digits[-10:]

        conn = get_db()

        orders = conn.execute("""
            SELECT *
            FROM orders
            WHERE
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    phone,
                                    ' ',
                                    ''
                                ),
                                '-',
                                ''
                            ),
                            '+',
                            ''
                        ),
                        '(',
                        ''
                    ),
                    ')',
                    ''
                ) LIKE ?
            ORDER BY id DESC
        """, (
            f"%{phone_digits}",
        )).fetchall()

        conn.close()

        if not orders:

            flash(
                "No orders found for this phone number.",
                "error"
            )

    return render_template(
        "find_order.html",
        orders=orders,
        searched_phone=searched_phone
    )


# ============================================================
# MY ORDERS
# ============================================================

@app.route("/my-orders")
@login_required
def my_orders():

    user_id = session["user_id"]

    conn = get_db()

    orders = conn.execute("""
        SELECT *
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "my_orders.html",
        orders=orders
    )


# ============================================================
# ORDER DETAIL
# ============================================================

@app.route(
    "/order/<int:order_id>"
)
def order_detail(order_id):

    conn = get_db()

    order = conn.execute("""
        SELECT *
        FROM orders
        WHERE id = ?
    """, (order_id,)).fetchone()

    if order is None:

        conn.close()

        abort(404)

    items = conn.execute("""
        SELECT
            oi.*,
            b.title,
            b.author,
            b.image
        FROM order_items oi
        JOIN books b
            ON oi.book_id = b.id
        WHERE oi.order_id = ?
    """, (order_id,)).fetchall()

    conn.close()

    return render_template(
        "order.html",
        order=order,
        items=items
    )


# ============================================================
# ADD REVIEW
# ============================================================

@app.route(
    "/book/<int:book_id>/review",
    methods=["POST"]
)
def add_review(book_id):

    name = request.form.get(
        "name",
        ""
    ).strip()

    rating = request.form.get(
        "rating",
        ""
    ).strip()

    comment = request.form.get(
        "comment",
        ""
    ).strip()

    if not name or not rating or not comment:

        flash(
            "All review fields are required.",
            "error"
        )

        return redirect(
            url_for(
                "book_detail",
                book_id=book_id
            )
        )

    try:

        rating = int(rating)

    except ValueError:

        flash(
            "Rating must be a number.",
            "error"
        )

        return redirect(
            url_for(
                "book_detail",
                book_id=book_id
            )
        )

    if rating < 1 or rating > 5:

        flash(
            "Rating must be between 1 and 5.",
            "error"
        )

        return redirect(
            url_for(
                "book_detail",
                book_id=book_id
            )
        )

    conn = get_db()

    book = conn.execute("""
        SELECT id
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    if book is None:

        conn.close()

        flash(
            "Book not found.",
            "error"
        )

        return redirect(
            url_for("home")
        )

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn.execute("""
        INSERT INTO reviews
        (
            book_id,
            name,
            rating,
            comment,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        book_id,
        name,
        rating,
        comment,
        created_at
    ))

    conn.commit()
    conn.close()

    flash(
        "Review added successfully.",
        "success"
    )

    return redirect(
        url_for(
            "book_detail",
            book_id=book_id
        )
    )


# ============================================================
# WISHLIST
# ============================================================

@app.route(
    "/wishlist"
)
@login_required
def wishlist():

    user_id = session["user_id"]

    conn = get_db()

    books = conn.execute("""
        SELECT
            b.*
        FROM wishlist w
        JOIN books b
            ON w.book_id = b.id
        WHERE w.user_id = ?
        ORDER BY w.id DESC
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "wishlist.html",
        books=books
    )


# ============================================================
# ADD TO WISHLIST
# ============================================================

@app.route(
    "/wishlist/add/<int:book_id>",
    methods=["POST"]
)
@login_required
def add_to_wishlist(book_id):

    user_id = session["user_id"]

    conn = get_db()

    book = conn.execute("""
        SELECT id
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    if book is None:

        conn.close()

        flash(
            "Book not found.",
            "error"
        )

        return redirect(
            url_for("home")
        )

    existing = conn.execute("""
        SELECT id
        FROM wishlist
        WHERE user_id = ?
        AND book_id = ?
    """, (
        user_id,
        book_id
    )).fetchone()

    if existing:

        conn.close()

        flash(
            "Book is already in your wishlist.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("home")
        )

    conn.execute("""
        INSERT INTO wishlist
        (
            user_id,
            book_id
        )
        VALUES (?, ?)
    """, (
        user_id,
        book_id
    ))

    conn.commit()
    conn.close()

    flash(
        "Book added to wishlist.",
        "success"
    )

    return redirect(
        request.referrer or
        url_for("home")
    )


# ============================================================
# REMOVE FROM WISHLIST
# ============================================================

@app.route(
    "/wishlist/remove/<int:book_id>",
    methods=["POST"]
)
@login_required
def remove_from_wishlist(book_id):

    user_id = session["user_id"]

    conn = get_db()

    conn.execute("""
        DELETE FROM wishlist
        WHERE user_id = ?
        AND book_id = ?
    """, (
        user_id,
        book_id
    ))

    conn.commit()
    conn.close()

    flash(
        "Book removed from wishlist.",
        "success"
    )

    return redirect(
        request.referrer or
        url_for("wishlist")
    )


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        admin = conn.execute("""
            SELECT *
            FROM admins
            ORDER BY id ASC
            LIMIT 1
        """).fetchone()

        conn.close()

        if admin and check_password_hash(
            admin["password_hash"],
            password
        ):

            session["admin_logged_in"] = True

            flash(
                "Admin login successful.",
                "success"
            )

            return redirect(
                url_for("admin_dashboard")
            )

        flash(
            "Invalid admin password.",
            "error"
        )

    return render_template(
        "admin_login.html"
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_logged_in",
        None
    )

    flash(
        "Admin logged out.",
        "success"
    )

    return redirect(
        url_for("admin_login")
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin")
@admin_required
def admin_dashboard():

    conn = get_db()

    books_count = conn.execute("""
        SELECT COUNT(*)
        FROM books
    """).fetchone()[0]

    users_count = conn.execute("""
        SELECT COUNT(*)
        FROM users
    """).fetchone()[0]

    orders_count = conn.execute("""
        SELECT COUNT(*)
        FROM orders
    """).fetchone()[0]

    revenue = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM orders
    """).fetchone()[0]

    recent_orders = conn.execute("""
        SELECT *
        FROM orders
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        books_count=books_count,
        users_count=users_count,
        orders_count=orders_count,
        revenue=revenue,
        recent_orders=recent_orders
    )
# ============================================================
# ADMIN ADD BOOK
# ============================================================

@app.route(
    "/admin/books/add",
    methods=["GET", "POST"]
)
@admin_required
def admin_add_book():

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        author = request.form.get(
            "author",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        price = request.form.get(
            "price",
            "0"
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        stock = request.form.get(
            "stock",
            "0"
        ).strip()

        cover_color = request.form.get(
            "cover_color",
            ""
        ).strip()

        image = request.form.get(
            "image",
            ""
        ).strip()

        if not title or not author or not category:

            flash(
                "Title, author and category are required.",
                "error"
            )

            return redirect(
                url_for("admin_add_book")
            )

        try:

            price = float(price)
            stock = int(stock)

        except ValueError:

            flash(
                "Price and stock must be valid numbers.",
                "error"
            )

            return redirect(
                url_for("admin_add_book")
            )

        conn = get_db()

        conn.execute("""
            INSERT INTO books
            (
                title,
                author,
                category,
                price,
                description,
                stock,
                cover_color,
                image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            author,
            category,
            price,
            description,
            stock,
            cover_color,
            image
        ))

        conn.commit()
        conn.close()

        flash(
            "Book added successfully.",
            "success"
        )

        return redirect(
            url_for("admin_dashboard")
        )

    return render_template(
        "admin_add_book.html"
    )


# ============================================================
# ADMIN DELETE BOOK
# ============================================================

@app.route(
    "/admin/books/delete/<int:book_id>",
    methods=["POST"]
)
@admin_required
def admin_delete_book(book_id):

    conn = get_db()

    try:

        conn.execute("""
            DELETE FROM books
            WHERE id = ?
        """, (book_id,))

        conn.commit()

        flash(
            "Book deleted successfully.",
            "success"
        )

    except sqlite3.IntegrityError:

        flash(
            "Book cannot be deleted because it is associated with an order.",
            "error"
        )

    finally:

        conn.close()

    return redirect(
        url_for("admin_dashboard")
    )


# ============================================================
# ADMIN COUPONS
# ============================================================

@app.route(
    "/admin/coupons",
    methods=["GET", "POST"]
)
@admin_required
def admin_coupons():

    conn = get_db()

    if request.method == "POST":

        code = request.form.get(
            "code",
            ""
        ).strip().upper()

        percent = request.form.get(
            "percent",
            "0"
        ).strip()

        if not code:

            conn.close()

            flash(
                "Coupon code is required.",
                "error"
            )

            return redirect(
                url_for("admin_coupons")
            )

        try:

            percent = float(percent)

        except ValueError:

            conn.close()

            flash(
                "Discount percentage must be a number.",
                "error"
            )

            return redirect(
                url_for("admin_coupons")
            )

        if percent <= 0 or percent > 100:

            conn.close()

            flash(
                "Discount percentage must be between 1 and 100.",
                "error"
            )

            return redirect(
                url_for("admin_coupons")
            )

        existing = conn.execute("""
            SELECT id
            FROM coupons
            WHERE code = ?
        """, (code,)).fetchone()

        if existing:

            conn.execute("""
                UPDATE coupons
                SET percent = ?
                WHERE code = ?
            """, (
                percent,
                code
            ))

            flash(
                "Coupon updated successfully.",
                "success"
            )

        else:

            conn.execute("""
                INSERT INTO coupons
                (
                    code,
                    percent
                )
                VALUES (?, ?)
            """, (
                code,
                percent
            ))

            flash(
                "Coupon added successfully.",
                "success"
            )

        conn.commit()

        return redirect(
            url_for("admin_coupons")
        )

    coupons = conn.execute("""
        SELECT *
        FROM coupons
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin_coupons.html",
        coupons=coupons
    )


# ============================================================
# ADMIN DELETE COUPON
# ============================================================

@app.route(
    "/admin/coupons/delete/<int:coupon_id>",
    methods=["POST"]
)
@admin_required
def admin_delete_coupon(coupon_id):

    conn = get_db()

    conn.execute("""
        DELETE FROM coupons
        WHERE id = ?
    """, (coupon_id,))

    conn.commit()
    conn.close()

    flash(
        "Coupon deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin_coupons")
    )


# ============================================================
# ADMIN REPORTS
# ============================================================

@app.route("/admin/reports")
@admin_required
def admin_reports():

    conn = get_db()

    total_books = conn.execute("""
        SELECT COUNT(*)
        FROM books
    """).fetchone()[0]

    total_users = conn.execute("""
        SELECT COUNT(*)
        FROM users
    """).fetchone()[0]

    total_orders = conn.execute("""
        SELECT COUNT(*)
        FROM orders
    """).fetchone()[0]

    total_revenue = conn.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM orders
    """).fetchone()[0]

    total_discount = conn.execute("""
        SELECT COALESCE(SUM(discount), 0)
        FROM orders
    """).fetchone()[0]

    category_data = conn.execute("""
        SELECT
            category,
            COUNT(*) AS count
        FROM books
        GROUP BY category
        ORDER BY count DESC
    """).fetchall()

    top_books = conn.execute("""
        SELECT
            b.title,
            b.author,
            SUM(oi.quantity) AS quantity_sold
        FROM order_items oi
        JOIN books b
            ON oi.book_id = b.id
        GROUP BY oi.book_id
        ORDER BY quantity_sold DESC
        LIMIT 10
    """).fetchall()

    recent_orders = conn.execute("""
        SELECT *
        FROM orders
        ORDER BY id DESC
        LIMIT 20
    """).fetchall()

    conn.close()

    return render_template(
        "admin_reports.html",
        total_books=total_books,
        total_users=total_users,
        total_orders=total_orders,
        total_revenue=total_revenue,
        total_discount=total_discount,
        category_data=category_data,
        top_books=top_books,
        recent_orders=recent_orders
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )