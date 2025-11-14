# Use a slim Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies (for psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copy the project
COPY . .

# Ensure uploads folder exists
RUN mkdir -p uploads

# Environment variables
ENV FLASK_APP=run.py \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run DB migrations then start Gunicorn
CMD ["bash", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:5000 run:app"]
