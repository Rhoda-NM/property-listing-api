# 🏡 Property Listing API — Flask RESTX + Docker + Postgres
<p align="center"> <img src="banner.png" width="100%" alt="Property Listing API Banner"/> </p>

A production-ready real estate backend built with:

🔥 Flask
🔥 Flask-RESTX (Swagger UI)
🔥 JWT Authentication
🔥 SQLAlchemy ORM + Flask-Migrate (Alembic)
🔥 Geo-Search (Haversine formula)
🔥 Image Uploads + File Serving
🔥 Docker + Postgres + Gunicorn

This project is designed as a portfolio showcase demonstrating clean architecture, advanced backend concepts, devops tooling, and API design skills.

## 🚀 Features
### 🔐 Authentication (JWT)

Register

Login

Agent vs Normal User roles

Only agents can create / update / delete listings and view messages

### 🏠 Listings

Full CRUD

Filters:

City

Bedrooms / bathrooms

Price range

Property type

Status (active, sold, etc.)

Sorting (date, price)

Pagination

Geo-based search using Haversine formula

Image uploads (local dev folder + URL responses)

### 🧑‍💼 Agents

List all agents

Search by name / email / company

Agent profile endpoint

Get listings belonging to an agent

### 💬 Messages

Public users send inquiries

Messages tied to listings

Agents view inbox for their own listings

Access control (agents only)

### 📅 Bookings

Users can book viewing dates

Prevent overlapping bookings

Agents confirm / reject bookings

Full CRUD logic

## ⚙️ Tech Stack

Backend Framework -	Flask
API Structure -	Flask-RESTX (Namespacing + Swagger)
Auth - Flask-JWT-Extended
ORM - SQLAlchemy
DB Migrations - Flask-Migrate / Alembic
Validation - Marshmallow
Database - SQLite (dev) → PostgreSQL (Docker prod)
File Uploads -	Werkzeug
Deployment Runtime - Gunicorn
Containerization -	Docker + docker-compose

## 📂 Project Structure
property-listing-api/
│── app/
│   ├── models/          # SQLAlchemy models
│   ├── resources/       # Flask-RESTX endpoints
│   ├── schemas/         # Marshmallow schemas
│   ├── extensions.py    # db, jwt, ma, migrate
│   ├── config.py        # configuration (env-based)
│   └── __init__.py      # app factory
│
│── migrations/          # Alembic migrations
│── uploads/             # image storage (dev)
│── docker-compose.yml
│── Dockerfile
│── seed.py              # sample data for demo
│── Makefile
│── requirements.txt
│── run.py
└── .env

## 📘 Swagger Documentation

Once the server is running:

👉 http://127.0.0.1:5000/docs

Swagger includes:

Example payloads

Query params

Response models

Organized namespaces

Try-it-out button

## 🛠️ Local Installation (SQLite Dev Mode)
1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Set environment variables

.env (example):

FLASK_ENV=development
SECRET_KEY=dev-secret
JWT_SECRET_KEY=jwt-secret
DATABASE_URL=sqlite:///property.db
UPLOAD_FOLDER=uploads

3. Run the server
python run.py


Visit:

Swagger → http://127.0.0.1:5000/docs

Health → http://127.0.0.1:5000/health

## 🧪 Database Migrations

Initialize migrations:

export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

## 🌱 Seed Sample Data

Generate demo listings, agents, bookings, and messages:

python seed.py

## 🐳 Docker Deployment (Postgres + Gunicorn)

This project includes a full production-style Docker setup.

1. Build and run:
docker-compose up --build

2. Containers:

db → PostgreSQL

web → Flask API served via Gunicorn

3. Data persists in:
docker volume: property-listing-api_db_data


Swagger remains available at:

👉 http://127.0.0.1:5000/docs

## 🛠️ Makefile (Developer Quality of Life)
run:
	python run.py

install:
	pip install -r requirements.txt

fmt:
	black app

migrate:
	 flask db migrate -m "auto"

upgrade:
	 flask db upgrade

## 🧪 Testing

Pytest + Flask test client:

pytest


## Covers:

Listings

Bookings (overlap rules)

Auth flow

REST behavior

## 🧑‍💻 Author

Rhoda Njeri Muya
Full-Stack Developer — React + Flask
🇰🇪 Kenya
GitHub: https://github.com/Rhoda-NM