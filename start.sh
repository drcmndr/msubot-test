#!/bin/bash
set -e

echo "Starting Rasa server..."
rasa run --enable-api --port $PORT --model models/20250219-213623-prompt-factor.tar.gz --cors "*"