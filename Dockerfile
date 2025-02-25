
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




FROM rasa/rasa:3.6.2-full

WORKDIR /app

# Create models directory if it doesn't exist
RUN mkdir -p /app/models

# Copy your model files
COPY models/ /app/models/

# Expose port
EXPOSE 10000

# Command to run the application
CMD rasa run --enable-api --port $PORT --model models/20250219-213623-prompt-factor.tar.gz --cors "*"