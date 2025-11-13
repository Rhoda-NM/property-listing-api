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

