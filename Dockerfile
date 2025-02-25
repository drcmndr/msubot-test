# FROM python:3.9.12-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     && rm -rf /var/lib/apt/lists/*

# # Upgrade pip
# RUN pip install --upgrade pip

# # Copy requirements first for better caching
# COPY requirements.txt .

# # Install dependencies in smaller chunks with retry logic
# RUN pip install --no-cache-dir flask==2.0.1 flask-cors==3.0.10 gunicorn==20.1.0 && \
#     pip install --no-cache-dir spacy==3.5.2 && \
#     pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0-py3-none-any.whl && \
#     pip install --no-cache-dir --timeout 600 tensorflow==2.12.0 && \
#     pip install --no-cache-dir --timeout 600 rasa==3.6.2

# # Create models directory
# RUN mkdir -p models

# # Copy the rest of the application
# COPY . .

# # Expose the port the app runs on
# EXPOSE 10000

# # Command to run the application
# CMD gunicorn --bind 0.0.0.0:10000 app:app



# # Dockerfile

# FROM python:3.9.12-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Upgrade pip
# RUN pip install --upgrade pip

# # Install minimal dependencies for serving
# RUN pip install --no-cache-dir flask==2.0.1 flask-cors==3.0.10 gunicorn==20.1.0

# # Copy the app and model first
# COPY app.py .
# COPY models/ models/

# # Now install Rasa with minimal dependencies
# # This installs only what's needed to run the model, not train it
# RUN pip install --no-cache-dir rasa==3.6.2 --only-binary=:all:

# # Copy the rest of the application
# COPY . .

# # Expose the port
# EXPOSE 10000

# # Command to run the application
# CMD gunicorn --bind 0.0.0.0:10000 app:app

# Dockerfile

FROM rasa/rasa:3.6.2-full

WORKDIR /app

# Copy your server script
COPY serve.py /app/

# Create models directory if it doesn't exist
RUN mkdir -p /app/models

# Copy your model files
COPY models/ /app/models/

# Expose port
EXPOSE 10000

# Command to run the application
CMD python serve.py