# 🏡 Property Listing API — Flask RESTX

A fully-featured real-estate backend built with **Flask**, **Flask-RESTX**, **JWT Authentication**, **SQLAlchemy**, and **Swagger UI**.

This project is production-structured and portfolio-ready.  
It demonstrates clean REST architecture, authentication, file uploads, geo-search, and relational data modeling.

---

## 🚀 Features

### **Authentication**
- Register / Login using JWT
- Agent vs Normal user permissions

### **Listings**
- CRUD operations
- Price filters, bedroom filters, city search
- Geo-based search using the Haversine formula
- Image uploads (local dev)
- Pagination + sorting

### **Agents**
- List agents
- Search agents (name, email, company)
- View agent profile + their listings

### **Messages**
- Public can send inquiries about a listing
- Agents can view inbox for their listings
- Agent-only message access

### **Bookings**
- Guests can request viewing/booking dates
- Prevent overlapping bookings
- Agents can confirm/cancel bookings

---

## 🧱 Tech Stack

- **Flask**
- **Flask-RESTX** (Swagger UI)
- **Flask-JWT-Extended**
- **Flask-Migrate** / Alembic
- **SQLAlchemy ORM**
- **Marshmallow Validation**
- **SQLite (dev)** → Upgrade to PostgreSQL for production
- **Werkzeug File Uploads**

---

## 📂 Project Structure

property-listing-api/
│── app/
│ ├── models/
│ ├── resources/
│ ├── schemas/
│ ├── extensions.py
│ ├── config.py
│ └── init.py
│── uploads/ # image storage in dev
│── requirements.txt
│── run.py
│── README.md
└── .env


---

## 📘 API Documentation (Swagger)

Once the server is running:

👉 http://127.0.0.1:5000/docs  

All endpoints are fully documented using Flask-RESTX.

---

## 🛠️ Installation & Setup

### Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


🧑‍💻 Author

Rhoda Njeri Muya
Full-Stack Developer | React + Flask
Kenya 🇰🇪
https://github.com/Rhoda-NM
