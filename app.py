from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import sqlite3
from pathlib import Path
from functools import wraps

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "bookstore.db"

app = Flask(__name__)
app.secret_key = "pageturner-dev-secret-key-change-me"


def get_db():
    """Open a SQLite connection and return rows like dictionaries."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables and add sample books the first time the app starts."""
    conn = get_db()
    schema = (BASE_DIR / "schema.sql").read_text(encoding="utf-8")
    conn.executescript(schema)

    book_count = conn.execute("SELECT COUNT(*) AS count FROM books").fetchone()["count"]
    if book_count == 0:
        seed = (BASE_DIR / "seed.sql").read_text(encoding="utf-8")
        conn.executescript(seed)

    conn.commit()
    conn.close()


def cart_count():
    return sum(session.get("cart", {}).values())


@app.context_processor
def inject_cart_count():
    return {"cart_count": cart_count()}


@app.route("/")
def home():
    category = request.args.get("category", "").strip()
    conn = get_db()

    if category:
        books = conn.execute(
            "SELECT * FROM books WHERE category = ? ORDER BY title",
            (category,)
        ).fetchall()
    else:
        books = conn.execute(
            "SELECT * FROM books ORDER BY title"
        ).fetchall()

    categories = conn.execute(
        "SELECT DISTINCT category FROM books ORDER BY category"
    ).fetchall()

    conn.close()
    return render_template(
        "home.html",
        books=books,
        categories=categories,
        selected_category=category
    )


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    conn = get_db()
    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()
    conn.close()

    if book is None:
        flash("Book not found.", "error")
        return redirect(url_for("home"))

    return render_template("book.html", book=book)


@app.post("/cart/add/<int:book_id>")
def add_to_cart(book_id):
    conn = get_db()
    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()
    conn.close()

    if book is None:
        flash("Book not found.", "error")
        return redirect(url_for("home"))

    cart = session.get("cart", {})
    key = str(book_id)
    current_quantity = int(cart.get(key, 0))

    if current_quantity >= book["stock"]:
        flash("You cannot add more than the available stock.", "error")
    else:
        cart[key] = current_quantity + 1
        session["cart"] = cart
        session.modified = True
        flash(f'"{book["title"]}" added to your cart.', "success")

    return redirect(request.referrer or url_for("home"))


@app.route("/cart")
def cart():
    cart_data = session.get("cart", {})
    items = []
    total = 0.0

    if cart_data:
        ids = [int(book_id) for book_id in cart_data.keys()]
        placeholders = ",".join(["?"] * len(ids))

        conn = get_db()
        books = conn.execute(
            f"SELECT * FROM books WHERE id IN ({placeholders})",
            ids
        ).fetchall()
        conn.close()

        book_map = {book["id"]: book for book in books}

        for book_id_string, quantity in cart_data.items():
            book_id = int(book_id_string)
            book = book_map.get(book_id)
            if book:
                quantity = int(quantity)
                subtotal = book["price"] * quantity
                items.append({
                    "book": book,
                    "quantity": quantity,
                    "subtotal": subtotal
                })
                total += subtotal

    return render_template("cart.html", items=items, total=total)


@app.post("/cart/update/<int:book_id>")
def update_cart(book_id):
    try:
        quantity = int(request.form.get("quantity", "0"))
    except ValueError:
        quantity = 0

    conn = get_db()
    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()
    conn.close()

    if book is None:
        flash("Book not found.", "error")
        return redirect(url_for("cart"))

    if quantity < 1:
        flash("Quantity must be at least 1.", "error")
        return redirect(url_for("cart"))

    if quantity > book["stock"]:
        flash(f"Only {book['stock']} copies are available.", "error")
        return redirect(url_for("cart"))

    cart_data = session.get("cart", {})
    key = str(book_id)

    if key in cart_data:
        cart_data[key] = quantity
        session["cart"] = cart_data
        session.modified = True
        flash("Cart updated.", "success")

    return redirect(url_for("cart"))


@app.post("/cart/remove/<int:book_id>")
def remove_from_cart(book_id):
    cart_data = session.get("cart", {})
    key = str(book_id)

    if key in cart_data:
        del cart_data[key]
        session["cart"] = cart_data
        session.modified = True
        flash("Book removed from your cart.", "success")

    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_data = session.get("cart", {})

    if not cart_data:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart"))

    conn = get_db()
    items = []

    for book_id_string, quantity in cart_data.items():
        book_id = int(book_id_string)
        book = conn.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,)
        ).fetchone()

        if book is None:
            continue

        quantity = int(quantity)
        if quantity > book["stock"]:
            conn.close()
            flash(f'Not enough stock for "{book["title"]}".', "error")
            return redirect(url_for("cart"))

        items.append({
            "book": book,
            "quantity": quantity,
            "subtotal": book["price"] * quantity
        })

    total = sum(item["subtotal"] for item in items)

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not customer_name or not phone or not address:
            conn.close()
            flash("All checkout fields are required.", "error")
            return render_template("checkout.html", items=items, total=total)

        if not phone.isdigit() or len(phone) != 10:
            conn.close()
            flash("Phone number must be exactly 10 digits.", "error")
            return render_template("checkout.html", items=items, total=total)

        # Recheck stock immediately before saving the order.
        for item in items:
            latest = conn.execute(
                "SELECT stock FROM books WHERE id = ?",
                (item["book"]["id"],)
            ).fetchone()
            if latest["stock"] < item["quantity"]:
                conn.close()
                flash(f'Not enough stock for "{item["book"]["title"]}".', "error")
                return redirect(url_for("cart"))

        try:
            cursor = conn.execute(
                """
                INSERT INTO orders (customer_name, phone, address, total, created_at)
                VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
                """,
                (customer_name, phone, address, total)
            )
            order_id = cursor.lastrowid

            for item in items:
                book_id = item["book"]["id"]
                quantity = item["quantity"]
                price = item["book"]["price"]

                conn.execute(
                    """
                    INSERT INTO order_items (order_id, book_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (order_id, book_id, quantity, price)
                )

                # Bonus feature: reduce stock after a successful order.
                conn.execute(
                    "UPDATE books SET stock = stock - ? WHERE id = ?",
                    (quantity, book_id)
                )

            conn.commit()
            session.pop("cart", None)
            conn.close()

            return redirect(url_for("order_confirmation", order_id=order_id))

        except sqlite3.Error:
            conn.rollback()
            conn.close()
            flash("Could not place the order. Please try again.", "error")
            return render_template("checkout.html", items=items, total=total)

    conn.close()
    return render_template("checkout.html", items=items, total=total)


@app.route("/order/<int:order_id>")
def order_confirmation(order_id):
    conn = get_db()

    order = conn.execute(
        "SELECT * FROM orders WHERE id = ?",
        (order_id,)
    ).fetchone()

    if order is None:
        conn.close()
        abort(404)

    items = conn.execute(
        """
        SELECT
            order_items.quantity,
            order_items.price,
            books.title,
            books.author
        FROM order_items
        JOIN books ON books.id = order_items.book_id
        WHERE order_items.order_id = ?
        ORDER BY order_items.id
        """,
        (order_id,)
    ).fetchall()

    conn.close()
    return render_template(
        "order.html",
        order=order,
        items=items
    )


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
