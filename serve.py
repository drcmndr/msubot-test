import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get port from environment
port = int(os.getenv('PORT', 10000))
model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

def main():
    logger.info(f"Starting Rasa server on port {port}")
    logger.info(f"Using model: {model_path}")
    
    # Check if model exists
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        sys.exit(1)
    
    # Start Rasa server
    cmd = [
        "rasa", "run",
        "--enable-api",
        f"--port={port}",
        f"--model={model_path}",
        "--cors=*"
    ]
    
    logger.info(f"Running command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(cmd)
        process.wait()
    except Exception as e:
        logger.error(f"Error starting Rasa server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()