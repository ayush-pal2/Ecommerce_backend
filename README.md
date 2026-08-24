# 🛒 E-Commerce Backend API (Django + DRF)

A scalable **E-Commerce Backend REST API** built with **Django** and **Django REST Framework (DRF)**.
It provides JWT-secured APIs for user authentication, role-based access control, hierarchical
categories, and product management — with soft-delete (bin/restore) support and Swagger/Redoc
API documentation built in.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment & Settings](#environment--settings)
  - [Database Setup](#database-setup)
  - [Run the Server](#run-the-server)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Roles & Permissions](#-roles--permissions)
- [API Reference](#-api-reference)
  - [Auth Endpoints](#auth-endpoints)
  - [Category Endpoints](#category-endpoints)
  - [Product Endpoints](#product-endpoints)
- [Soft Delete (Bin & Restore)](#-soft-delete-bin--restore)
- [Pagination](#-pagination)
- [Logging](#-logging)
- [Running Tests](#-running-tests)
- [Known Issues / Improvement Ideas](#-known-issues--improvement-ideas)
- [Contributing](#-contributing)

---

## 🚀 Features

- **User Authentication** — Register & Login with JWT (JSON Web Tokens)
- **Role-Based Access Control** — `Admin` and `Customer` roles, enforced via a custom `IsAdmin` permission
- **Category Management** — Nested (parent/child) categories with recursive tree serialization
- **Product Management** — Full CRUD operations linked to categories
- **Soft Delete Support** — Categories and products are moved to a "bin" instead of being permanently deleted, and can be restored (deleting a category cascades the soft-delete to its subcategories and products)
- **Pagination** — Page-number based pagination on list endpoints
- **API Docs** — Auto-generated Swagger UI and ReDoc via `drf-yasg`
- **Structured Logging** — Key actions (creates, updates, deletes, auth events) are logged to console/`ecommerce.log`

---

## 🛠 Tech Stack

| Layer            | Technology                              |
|-------------------|------------------------------------------|
| Language           | Python 3                                |
| Framework          | Django 5.1.1                            |
| API Toolkit        | Django REST Framework (DRF)             |
| Auth               | `djangorestframework-simplejwt` (JWT)   |
| API Docs           | `drf-yasg` (Swagger / ReDoc)            |
| Database (default) | SQLite3 (swappable via `DATABASES`)     |

---

## 📁 Project Structure

```
Ecommerce_backend-main/
├── ecommerce/                 # Project configuration
│   ├── settings.py            # Django settings (apps, DB, JWT, DRF, logging)
│   ├── urls.py                # Root URL routes + Swagger/Redoc + auth routes
│   ├── wsgi.py / asgi.py
│
├── categories/                 # Users & Categories app
│   ├── models.py               # `User` (custom AbstractUser) & `Category` models
│   ├── permissions.py          # `IsAdmin` custom permission
│   ├── utils.py                # Recursive soft-delete / restore helpers
│   ├── urls.py                 # Category route definitions
│   ├── serializers.py
│   ├── views/
│   │   ├── user_views.py       # register / login_user
│   │   └── categories_views.py # Category CRUD + bin/restore
│   └── migrations/
│
├── product/                     # Products app
│   ├── models.py                # `Product` model (linked to Category)
│   ├── serializers.py           # `ProductSerializer`
│   ├── forms.py
│   ├── urls.py                  # Product route definitions
│   ├── views.py                 # Product CRUD
│   └── migrations/
│
├── db.sqlite3                   # Default local database
├── ecommerce.log                # Application log file
└── manage.py                    # Django management entry point
```

---

## ⚡ Getting Started

### Prerequisites

- Python 3.10+ (project uses Django 5.1.1, which requires Python ≥ 3.10)
- `pip` and (recommended) `virtualenv`

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/Ecommerce_backend.git
   cd Ecommerce_backend-main
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   > This project doesn't ship a `requirements.txt` yet — install the packages below, or generate one with `pip freeze > requirements.txt` once installed.

   ```bash
   pip install django==5.1.1
   pip install djangorestframework
   pip install djangorestframework-simplejwt
   pip install drf-yasg
   ```

### Environment & Settings

The project currently keeps its configuration directly in `ecommerce/settings.py`. Before deploying (or pushing this repo publicly), you should externalize the sensitive values below into environment variables (e.g. using `python-decouple` or `django-environ`) instead of leaving them hard-coded:

| Setting        | Current Value (dev)                  | Recommendation                              |
|-----------------|----------------------------------------|-----------------------------------------------|
| `SECRET_KEY`    | Hard-coded in `settings.py`            | Move to an environment variable              |
| `DEBUG`         | `True`                                 | Set to `False` in production                 |
| `ALLOWED_HOSTS` | `[]`                                    | Add your domain/host in production           |

### Database Setup

The project uses **SQLite** out of the box (`db.sqlite3`), so no extra database server is required for local development.

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin user (useful for the Django admin site and for testing admin-only endpoints):

```bash
python manage.py createsuperuser
```

> Note: the custom `User` model has a `role` field (`admin` / `customer`, default `customer`). If you want a superuser with API-level admin permissions, set `role="admin"` on that user (e.g. via the Django admin, shell, or by registering through the API with `"role": "admin"`).

### Run the Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

---

## 📘 API Documentation

Interactive, auto-generated API docs are available once the server is running:

| Docs      | URL                                      |
|-----------|-------------------------------------------|
| Swagger UI | `http://127.0.0.1:8000/swagger/`         |
| ReDoc      | `http://127.0.0.1:8000/redoc/`           |
| Django Admin | `http://127.0.0.1:8000/admin/`         |

---

## 🔐 Authentication

Authentication is handled with **JWT** via `djangorestframework-simplejwt`.

1. Register a user via `POST /register/user`
2. Log in via `POST /login/user` to receive an `access` token
3. Include the token on subsequent requests:

   ```
   Authorization: Bearer <access_token>
   ```

> ⚠️ The access token lifetime is currently set to **1 minute** (`SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]`) in `settings.py`. This is fine for testing token expiry, but you'll likely want to increase it (and add refresh-token support in the URLs) for real usage.

---

## 👥 Roles & Permissions

The custom `User` model includes a `role` field:

| Role       | Description                                                       |
|-------------|---------------------------------------------------------------------|
| `customer` | Default role. Can view categories/products (read-only access).     |
| `admin`    | Full access — create/update/delete categories & products, view bin, restore deleted items. |

Admin-only endpoints are protected with a custom `IsAdmin` permission class, combined with `IsAuthenticated`.

---

## 📚 API Reference

> All endpoints are prefixed with the server base URL, e.g. `http://127.0.0.1:8000`.

### Auth Endpoints

| Method | Endpoint         | Access     | Description                          |
|--------|-------------------|------------|----------------------------------------|
| POST   | `/register/user`  | Public     | Register a new user (`username`, `password`, optional `role`) |
| POST   | `/login/user`      | Public     | Log in and receive a JWT `access` token |

**Register — request body**
```json
{
  "username": "john_doe",
  "password": "StrongPass123",
  "role": "customer"
}
```

**Login — request body**
```json
{
  "username": "john_doe",
  "password": "StrongPass123"
}
```

**Login — response**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "",
  "access": "<jwt-access-token>"
}
```

### Category Endpoints

Base path: `/categories/`

| Method | Endpoint                          | Access        | Description                                   |
|--------|-------------------------------------|---------------|-------------------------------------------------|
| GET    | `/categories/get/?page=&limit=`     | Public        | List top-level categories (with nested children), paginated |
| GET    | `/categories/getbyid/<id>`          | Public        | Get a single category (with nested children) by ID |
| POST   | `/categories/create`                | Admin only    | Create a category (`name`, optional `parent`) |
| PUT    | `/categories/putcategory/<id>`      | Admin only    | Fully update a category (`name`, `parent`)    |
| PATCH  | `/categories/patchcategory/<id>`    | Admin only    | Partially update a category                   |
| DELETE | `/categories/delete`                | Admin only    | Soft-delete a category (and its subtree) — body: `{"id": <id>}` |
| GET    | `/categories/bin/`                  | Admin only    | List soft-deleted categories                  |
| POST   | `/categories/restore/`              | Admin only    | Restore a soft-deleted category (and its subtree) — body: `{"id": <id>}` |

### Product Endpoints

Base path: `/product/`

| Method | Endpoint                              | Access        | Description                                |
|--------|------------------------------------------|---------------|-----------------------------------------------|
| GET    | `/product/get?page=&limit=`              | Authenticated | List products (excludes soft-deleted / deleted categories), paginated |
| GET    | `/product/getbyid/<id>`                   | Public        | List products belonging to a given category ID |
| POST   | `/product/create`                         | Admin only    | Create a product (`name`, `price`, `category`) |
| PUT    | `/product/updatefull/<id>`                | Admin only    | Fully update a product                       |
| PATCH  | `/product/updatepartially/<id>`           | Admin only    | Partially update a product                   |
| DELETE | `/product/delete`                         | Admin only    | Soft-delete a product — body: `{"id": <id>}` |

**Product — create request body**
```json
{
  "name": "Wireless Mouse",
  "price": 19.99,
  "category": 3
}
```

---

## 🗑 Soft Delete (Bin & Restore)

Instead of hard-deleting records, this project **soft-deletes** them by flipping an `is_deleted` flag:

- Deleting a **category** recursively soft-deletes all of its subcategories **and** the products under them (`soft_delete_category_tree`).
- Restoring a category recursively restores its subcategories and their products (`restore_category`).
- Deleting a **product** simply flags it as `is_deleted=True`.
- List/detail endpoints filter out `is_deleted=True` records so removed items disappear from normal views while remaining recoverable from the bin.

---

## 📄 Pagination

List endpoints (`categories/get/`, `product/get`) support standard page-based pagination via query parameters:

```
GET /product/get?page=2&limit=10
```

- `page` — page number (default `1`)
- `limit` — items per page (defaults: `5` for categories, `10` for products)

Response shape:
```json
{
  "count": 42,
  "results": [ ... ]
}
```

---

## 🧾 Logging

Key events (user registration, category/product create/update/delete, permission failures, etc.) are logged using Python's `logging` module, configured in `settings.py` to stream to the console. A running log is also written to `ecommerce.log` in the project root.

---

## ✅ Running Tests

Each app includes a `tests.py` file for Django's built-in test runner:

```bash
python manage.py test
```

---

## 🧩 Known Issues / Improvement Ideas

These are things worth addressing as the project matures — useful context for contributors:

- **No `requirements.txt`** — add one (`pip freeze > requirements.txt`) so setup is reproducible.
- **Hard-coded `SECRET_KEY` & `DEBUG=True`** — move to environment variables before any public/production deployment.
- **`rest_framework_simplejwt` isn't in `INSTALLED_APPS`** — it currently works because only the JWT authentication class and token view are used directly, but consider adding it explicitly if you use its models/migrations.
- **Access token lifetime is 1 minute** and there's no refresh-token endpoint wired up in `urls.py` — consider adding `TokenRefreshView` and a longer/more practical `ACCESS_TOKEN_LIFETIME`.
- **`product_create`** currently passes a queryset (not a single instance) into `category=category` — worth double-checking (`Category.objects.filter(...).first()`).
- No Cart / Wishlist / Order / Checkout implementation yet, despite being mentioned as planned features — these are natural next additions.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---
