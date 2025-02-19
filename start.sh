#!/bin/bash
# start.sh

echo "Starting Rasa server..."
rasa run --enable-api --cors "*" --port $PORT --model models/20250219-213623-prompt-factor.tar.gz --endpoints endpoints.yml &

# Wait for the port to be available
echo "Waiting for port $PORT..."
python check_port.py $PORT

echo "Rasa server is ready!"