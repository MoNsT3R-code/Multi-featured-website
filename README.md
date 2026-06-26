# The Artisan's Touch: Premium Resin Art Storefront

A high-performance, responsive E-Commerce web application designed for interactive art catalog manipulation, secure multi-tier session cart compilation, and back-office customer data management.

![Language](https://img.shields.io/badge/Language-Python%203.13+-blue?logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-Flask%203.0+-black?logo=flask&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite-blueviolet?logo=sqlite&logoColor=white)
![ORM Layer](https://img.shields.io/badge/ORM-SQLAlchemy%203.1-red?logo=databricks&logoColor=white)
![Architecture](https://img.shields.io/badge/Pattern-Monolith%20%2F%20RBAC-green)
![Storage](https://img.shields.io/badge/Persistence-Session%20Cookies-lightgrey)

---

## 🌐 Engine Overview

The Artisan's Touch combines transactional client storefront elements with an integrated, secure back-office administrative control dashboard. By utilizing object-relational database mapping, strict session boundary validators, and secure state handling, the platform decouples guest and consumer feature sets from system-level database management operations without needing complex, heavy multi-tier microservice architectures.

---

## 📍 Quick Navigation

* [🌐 Engine Overview](https://www.google.com/search?q=%23-engine-overview)
* [📦 System Architecture](https://www.google.com/search?q=%23-system-architecture)
* [✨ Key Architecture Features](https://www.google.com/search?q=%23-key-architecture-features)
* [📁 Repository Structure and Module Index](https://www.google.com/search?q=%23-repository-structure-and-module-index)
* [🛠️ Tech Stack](https://www.google.com/search?q=%23%25EF%25B8%258F-tech-stack)
* [💻 System Requirements](https://www.google.com/search?q=%23-system-requirements)
* [🚀 Setup & Execution Guide](https://www.google.com/search?q=%23-setup--execution-guide)
* [📊 Application Core Interfaces](https://www.google.com/search?q=%23-application-core-interfaces)
* [🏗️ Architectural Highlights](https://www.google.com/search?q=%23-architectural-highlights)

---

## 📦 System Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                       USER INTERACTION LAYER                 │
├──────────────────────────────────────────────────────────────┤
│               Browser DOM / Link Navigation Target           │
│        (Client Shop Frame [_self], Admin Reports [_blank])    │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│               OBJECT-ORIENTED APPLICATION CORE               │
├────────────┬─────────────┬────────────┬─────────────┬────────┤
│   Flask    │ SQLAlchemy  │ Role-Based │ Session-Cart│ Jinja2 │
│ App Engine │ Relational  │ Access     │ Dynamic Memory│ Secure │
│  (web.py)  │ Data Models │ Guardrails │ Interceptor │Template│
└────────────┴─────────────┴────────────┴─────────────┴────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                     DYNAMIC RENDERING AGENT                  │
├──────────────────────────────────────────────────────────────┤
│           Responsive Web Framework / Print Layout Engine     │
└──────────────────────────────────────────────────────────────┘

```

| Architectural Layer | Core Components & Strategies | Target Document Context |
| --- | --- | --- |
| **Top: Interaction** | Client Navigations / Report Views | Browsing (`target="_self"`) / Print View (`target="_blank"`) |
| **Middle: App Core** | Python Flask, SQLAlchemy Models, RBAC Security Guards | Core Server Infrastructure Pipeline (`web.py`) |
| **Bottom: Rendering** | Fluid CSS Grid Interfaces & Jinja2 Template Compilers | Client Base Shell Framework (`layout.html`) |

---

## ✨ Key Architecture Features

✅ **Role-Based Access Control (RBAC)** - Implements strict structural boundaries via wrapper decorators separating unauthenticated client view layouts from secure administrative routes (`/admin/*`).

✅ **State Lifecycle Boundary Tracking** - Explicitly protects active transactional operations by storing consumer shopping lists safely within secure client-side cookie containers (`session['cart']`).

✅ **Target Isolation Routing Rules** - Enforces unified session tracking by locking storefront pathways to standard targets (`target="_self"`), while launching standalone printable billing reports inside separate view panels (`target="_blank"`).

✅ **Persistent Database Model Mapping** - Configures data definitions cleanly using declarative entity classes (`User`, `Product`, `Order`, `OrderItem`) with corresponding structural relationships.

✅ **Robust Parameter Exception Interception** - Protects incoming transactional parameters from system exceptions by filtering non-numeric values and execution anomalies gracefully before database operations are committed.

---

## 📁 Repository Structure and Module Index

The project codebase is organized into the following logical components:

### Structural Framework Modules

* **`templates/layout.html`** - Master HTML5 base configuration managing common navigation links, user tracking tabs, and application status notices.

### Layout Styling

* **`templates/layout.html` inside `<style>**` - Core presentation engine managing fluid layout parameters, card grids, alert themes, and print rules.

### Functional Engines

* **`web.py`** - Core Python app containing system configuration vectors, operational routes, database schema arrays, and testing seed arrays.

---

## 🛠️ Tech Stack

| Component | Technology | Reference Scope |
| --- | --- | --- |
| **Core Framework** | Python 3.13+ & Flask 3.0.3 | Backend Processing Pipeline |
| **Database Engine** | Embedded SQLite Relational Engine | Local Storage Matrix Layer |
| **ORM Wrapper** | Flask-SQLAlchemy 3.1.1 | Relational Data Object Transformer |
| **Interface Agent** | Jinja2 Template Framework Engine | Dynamic HTML Rendering Controller |
| **Security Link** | Werkzeug Cryptography Hashing | Cryptographic Password Verification |

---

## 💻 System Requirements

Ensure your execution environment adheres to the following baseline parameters:

* **Execution Runtime:** Python 3.13+ platform setup containing standard package management tools (`pip`).
* **Display Layout Scale:** Adaptive responsive layouts down to 320px screen profiles; optimized for modern browser engines.
* **Network Status:** Fully functional under completely offline configurations (Zero remote content distribution requirements).

---

## 🚀 Setup & Execution Guide

### Step 1: Establish Workspace Directory

Create a dedicated workspace layout on your system file tree matching this path distribution:

```bash
Project-root/
        ├── web.py
        └── templates/
                ├── layout.html
                ├── home.html
                ├── shop.html
                ├── product_detail.html
                ├── cart.html
                ├── checkout.html
                ├── orders.html
                ├── about.html
                ├── login.html
                └── register.html

```

### Step 2: Implement Component Dependencies

Open a command terminal, navigate to your execution folder path, and execute the following dependency deployment:

```bash
python -m pip install Flask==3.0.3 Flask-SQLAlchemy==3.1.1 Werkzeug==3.0.3

```

### Step 3: Run the Application Locally

Launch your core application file to build the system layout, write the database tables, and run the developer server:

```bash
python web.py

```

Open your web browser and direct your request link to the development address:
👉 **`http://127.0.0.1:5000`**

---

## 📊 Application Core Interfaces

The system engine divides its platform operations across distinct structural segments:

| Panel Container | Access Authentication | Operational Purpose | Default Target Context |
| --- | --- | --- | --- |
| **Client Storefront** | Anonymous/Guest Allowed | Handles item browsing, descriptive specification views, and shopping cart manipulation. | `target="_self"` |
| **Checkout Pipeline** | Registered Client Verified | Processes delivery target registration details and updates systemic order logs. | `target="_self"` |
| **Admin Control Terminal** | Secured Administrative Key | Controls catalog item updates, order workflow status tracking, and database audits. | `target="_self"` |
| **Billing Summaries** | Secured Administrative Key | Renders clean, printer-ready transactional profile reports into independent sandbox frames. | `target="_blank"` |

---

## 🏗️ Architectural Highlights

### 🎨 Integrated Custom Properties

Manages color layouts and interface hierarchy variables using functional CSS variables built directly into the core document structure:

* `--primary-color`: `#1a365d` (Deep Slate Blue Foundation)
* `--accent-color`: `#d69e2e` (Muted Gold Artisan Highlight)
* `--surface-card`: `#ffffff` (Elevated Operational Panels)

### 🔐 Multi-Tier Security Verification

Ensures endpoint privacy by validating user account roles before executing functional methods. Requests to admin paths (`/admin/*`) from unauthorized users are intercepted, rejected, and forced onto verification screens with clear operational access errors.

### 📐 Automated Database Initialization

## Automatically detects missing asset tables at system boot, configures the native SQLite environment file, and drops default sample product listings (Clocks, Bookmarks, and Custom Decor) straight into data structures.

## 📄 License & Terms

This project is open-source. Feel free to copy, modify, and redistribute the single-page calculation dashboard application framework as required.
