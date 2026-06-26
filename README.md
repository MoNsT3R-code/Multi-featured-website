# The Artisan's Touch 🎨✨

An elegant, fully functional E-Commerce web application built for a premium liquid resin art storefront. The system features a distinct separation between customer browsing and secure administrative database management.

## 🚀 Architectural Overview

This platform is engineered using a clean monolithic structure powered by **Python (Flask)** and an **SQLite** database using **Flask-SQLAlchemy** as the Object-Relational Mapper (ORM).

### Key Features
*   **Role-Based Access Control (RBAC):** Strict security boundaries separating Client interfaces from secure Admin endpoints (`/admin/`).
*   **Persistent Shopping Session:** Dynamic, session-based cart memory allowing users to add, aggregate, and calculate order totals in real-time.
*   **Admin Control Panel:** Complete CRUD capabilities over the product catalog, order pipeline updates, and customer data audits.
*   **External Reporting Outflow:** Generates clean, printer-friendly operational summary profiles for clients that isolate securely in target view tabs (`_blank`).

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.13+, Flask
*   **Database ORM:** SQLite, Flask-SQLAlchemy
*   **Frontend:** Semantic HTML5, CSS3 Custom Properties (Variables), Vanilla JavaScript

---

## 📦 Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.13 or newer installed on your operating system.

### 2. Environment Configuration
Navigate to your project root directory and install the required dependencies:
```bash
pip install Flask==3.0.3 Flask-SQLAlchemy==3.1.1 Werkzeug==3.0.3

```

*(Alternatively, if using a requirements file: `pip install -r requirements.txt`)*

### 3. Launching the Engine

Run the core deployment file to initialize the local database schema and start the server:

```bash
python web.py

```

The application will initialize its database tables, seed mock items, and deploy a local pipeline engine at:
👉 **`http://127.0.0.1:5000`**

---

## 🔒 Testing Profiles

To audit administrative capabilities directly without passing a registration phase, use the system default testing parameters:

* **Username:** `admin`
* **Password:** `admin123`

```

```
