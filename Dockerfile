FROM python:3.9.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies in smaller chunks with retry logic
RUN pip install --no-cache-dir flask==2.0.1 flask-cors==3.0.10 gunicorn==20.1.0 && \
    pip install --no-cache-dir spacy==3.5.2 && \
    pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0-py3-none-any.whl && \
    pip install --no-cache-dir --timeout 600 tensorflow==2.12.0 && \
    pip install --no-cache-dir --timeout 600 rasa==3.6.2

# Create models directory
RUN mkdir -p models

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 10000

# Command to run the application
CMD gunicorn --bind 0.0.0.0:10000 app:app