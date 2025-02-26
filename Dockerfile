
# Dockerfile

# FROM rasa/rasa:3.6.2-full

# WORKDIR /app

# # Copy your server script
# COPY serve.py /app/

# # Create models directory if it doesn't exist
# RUN mkdir -p /app/models

# # Copy your model files
# COPY models/ /app/models/

# # Expose port
# EXPOSE 10000

# # Command to run the application
# CMD python serve.py




# Dockerfile

FROM rasa/rasa:3.6.2-full

WORKDIR /app

# Install additional dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY . /app/

# Create models directory if it doesn't exist
RUN mkdir -p /app/models

# Make start script executable
RUN chmod +x /app/start.sh

# Set environment variables
ENV PORT=10000
ENV RASA_MODEL=models/20250219-213623-prompt-factor.tar.gz

# Expose port
EXPOSE 10000

# Start Flask server
CMD ["python", "app.py"]