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
