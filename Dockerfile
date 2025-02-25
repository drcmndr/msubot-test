
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

# Create models directory
RUN mkdir -p /app/models

# Copy your model files
COPY models/ /app/models/

# Copy start script
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 10000

# Start Rasa server
CMD ["/app/start.sh"]