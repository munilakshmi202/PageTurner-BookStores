# PageTurner BookStore — Feature Guide and Run Instructions

## Start
1. Extract this ZIP.
2. Open `PageTurner_BookStore/PageTurner_BookStore` in VS Code.
3. Run `python -m pip install -r requirements.txt`.
4. Run `python app.py`.
5. Open `http://127.0.0.1:5000`.

Back up your `.db` files before schema changes.

## Steps 28–41: where to access features
- **28 Shipping address book:** log in as a customer → Addresses; checkout can select a saved address.
- **29 Multiple items per order:** add multiple books → Cart → Checkout → order details / My Orders.
- **30 Roles and permissions:** Admin Dashboard → Users; staff can access Manage Orders.
- **31 Password reset:** Login → Forgot Password. Reset links are shown in-app for development.
- **32 Login protection:** repeated failed logins are temporarily blocked.
- **33 CSRF:** POST forms use a hidden `csrf_token`; missing or incorrect tokens are rejected.
- **34 Inventory history:** use the per-book stock-history route from the admin stock-management workflow.
- **35 Cancel order:** My Orders; only Placed orders should be cancellable.
- **36 Recommendations:** open a book details page → Customers also bought.
- **37 Analytics dashboard:** Admin → Advanced Analytics.
- **38 Image upload:** Admin → Add/Edit Book; JPG, PNG or WEBP under 1 MB.
- **39 Blueprints/factory:** `factory.py`, `config.py`, `db.py`, and `security.py` exist, but full migration of every legacy HTML route into separate auth/shop/admin/api Blueprints remains incomplete.
- **40 Tests:** `python -m unittest discover -s tests -v`.
- **41 Final defence:** see `FINAL_DEFENCE.md`.

A visible link is not proof that the underlying feature works. Run tests and manually verify acceptance cases.
