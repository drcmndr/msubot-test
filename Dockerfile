FROM python:3.9.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir -p models

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 10000

# Command to run the application
CMD gunicorn --bind 0.0.0.0:10000 app:app