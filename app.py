
# # app.py

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import asyncio
# import os
# import sys
# import glob
# import logging
# import tensorflow as tf

# # Suppress tensorflow logging
# tf.get_logger().setLevel('ERROR')
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# app = Flask(__name__)

# # Configure CORS
# CORS(app, 
#      resources={
#          r"/*": {
#              "origins": ["http://localhost:8000", "http://127.0.0.1:8000", 
#                         "http://localhost:5500", "http://127.0.0.1:5500"],
#              "methods": ["GET", "POST", "OPTIONS"],
#              "allow_headers": ["Content-Type"],
#              "max_age": 3600
#          }
#      })

# def get_latest_model():
#     models_dir = 'models'
#     if not os.path.exists(models_dir):
#         os.makedirs(models_dir)
#         raise FileNotFoundError(f"Created new models directory at {models_dir}")
    
#     model_files = glob.glob(os.path.join(models_dir, '*.tar.gz'))
#     if not model_files:
#         raise FileNotFoundError(f"No model files found in {models_dir}")
    
#     latest_model = max(model_files, key=os.path.getmtime)
#     print(f"Loading model: {latest_model}")
#     return latest_model

# try:
#     model_path = get_latest_model()
#     agent = Agent.load(model_path)
#     print("Model loaded successfully!")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     raise

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# async def webhook():
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
#         return response, 200
        
#     try:
#         data = request.json
#         message = data.get('message')
#         sender_id = data.get('sender', 'default')
        
#         print(f"Received message: {message} from sender: {sender_id}")
        
#         if not message:
#             return jsonify({"error": "No message provided"}), 400
        
#         responses = await agent.handle_text(message)
#         print(f"Bot responses: {responses}")
        
#         formatted_responses = []
#         for response in responses:
#             if isinstance(response, dict) and 'text' in response:
#                 formatted_responses.append({
#                     'recipient_id': sender_id,
#                     'text': response['text']
#                 })
#             elif isinstance(response, str):
#                 formatted_responses.append({
#                     'recipient_id': sender_id,
#                     'text': response
#                 })
        
#         return jsonify(formatted_responses)
        
#     except Exception as e:
#         print(f"Error processing message: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     cli = sys.modules['flask.cli']
#     cli.show_server_banner = lambda *x: None
#     print("\nRasa webhook server is running on http://localhost:5005")
#     app.run(host='0.0.0.0', port=5005, debug=True)





# # app.py

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import asyncio
# import os
# import sys
# import glob
# import logging
# import tensorflow as tf

# # Suppress tensorflow logging
# tf.get_logger().setLevel('ERROR')
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)

# # Configure CORS for production
# CORS(app, 
#      resources={
#          r"/*": {
#              "origins": [
#                  "http://localhost:8000",
#                  "http://127.0.0.1:8000",
#                  "http://localhost:5500",
#                  "http://127.0.0.1:5500",
#                  "https://msubot-test.onrender.com",  # Your Render backend URL
#                  "https://drcmndr.github.io", # Your Pages frontend URL
#                  "https://drcmndr.github.io/msubot-frontend",
#                  "*"  # Temporarily allow all origins for testing
#              ],
#              "methods": ["GET", "POST", "OPTIONS"],
#              "allow_headers": ["Content-Type"],
#              "expose_headers": ["Content-Type"],
#              "supports_credentials": True,
#              "max_age": 3600
#          }
#      })

# def get_latest_model():
#     models_dir = 'models'
#     if not os.path.exists(models_dir):
#         os.makedirs(models_dir)
#         logger.warning(f"Created new models directory at {models_dir}")
#         return None
    
#     model_files = glob.glob(os.path.join(models_dir, '*.tar.gz'))
#     if not model_files:
#         logger.warning(f"No model files found in {models_dir}")
#         return None
    
#     latest_model = max(model_files, key=os.path.getmtime)
#     logger.info(f"Loading model: {latest_model}")
#     return latest_model

# # Initialize Rasa agent
# try:
#     model_path = get_latest_model()
#     if model_path:
#         agent = Agent.load(model_path)
#         logger.info("Model loaded successfully!")
#     else:
#         logger.warning("No model available. Please train the model first.")
#         agent = None
# except Exception as e:
#     logger.error(f"Error loading model: {e}")
#     agent = None

# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         "status": "healthy",
#         "model_status": "loaded" if agent else "not_loaded",
#         "model_path": model_path if model_path else None
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# async def webhook():
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         # Configure CORS headers for the OPTIONS response
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept')
#         response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
#         response.headers.add('Access-Control-Expose-Headers', 'Content-Type')
#         return response, 200
        
#     if not agent:
#         return jsonify({"error": "No model loaded. Please train the model first."}), 503
        
#     try:
#         data = request.json
#         message = data.get('message')
#         sender_id = data.get('sender', 'default')
        
#         logger.info(f"Received message: {message} from sender: {sender_id}")
        
#         if not message:
#             return jsonify({"error": "No message provided"}), 400
        
#         responses = await agent.handle_text(message)
#         logger.info(f"Bot responses: {responses}")
        
#         formatted_responses = []
#         for response in responses:
#             if isinstance(response, dict) and 'text' in response:
#                 formatted_responses.append({
#                     'recipient_id': sender_id,
#                     'text': response['text']
#                 })
#             elif isinstance(response, str):
#                 formatted_responses.append({
#                     'recipient_id': sender_id,
#                     'text': response
#                 })
        
#         # Add CORS headers to the response
#         response = jsonify(formatted_responses)
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Expose-Headers', 'Content-Type')
#         return response
        
#     except Exception as e:
#         logger.error(f"Error processing message: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5005))
#     logger.info(f"\nRasa webhook server is running on http://0.0.0.0:{port}")
#     app.run(host='0.0.0.0', port=port, debug=False)







# app.py

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import asyncio
# import os
# import sys
# import glob
# import logging
# import tensorflow as tf

# # Suppress tensorflow logging
# tf.get_logger().setLevel('ERROR')
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)

# # Configure CORS for production
# CORS(app, 
#      resources={
#          r"/*": {
#              "origins": [
#                  "http://localhost:8000",
#                  "http://127.0.0.1:8000",
#                  "http://localhost:5500",
#                  "http://127.0.0.1:5500",
#                  "https://msubot-test.onrender.com",
#                  "https://drcmndr.github.io",
#                  "https://drcmndr.github.io/msubot-frontend",
#                  "*"
#              ],
#              "methods": ["GET", "POST", "OPTIONS"],
#              "allow_headers": ["Content-Type"],
#              "expose_headers": ["Content-Type"],
#              "supports_credentials": True,
#              "max_age": 3600
#          }
#      })

# # Initialize Rasa agent globally
# try:
#     model_path = "models/20250219-213623-prompt-factor.tar.gz"  # Your specific model
#     agent = Agent.load(model_path)
#     logger.info("Model loaded successfully!")
# except Exception as e:
#     logger.error(f"Error loading model: {e}")
#     agent = None

# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({"status": "Rasa server is running"})

# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         "status": "healthy",
#         "model_status": "loaded" if agent else "not_loaded",
#         "model_path": model_path if 'model_path' in locals() else None
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# async def webhook():
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept')
#         response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
#         response.headers.add('Access-Control-Expose-Headers', 'Content-Type')
#         return response, 200
        
#     if not agent:
#         return jsonify({"error": "No model loaded. Please train the model first."}), 503
        
#     try:
#         data = request.json
#         message = data.get('message')
#         sender_id = data.get('sender', 'default')
        
#         logger.info(f"Received message: {message} from sender: {sender_id}")
        
#         if not message:
#             return jsonify({"error": "No message provided"}), 400
        
#         responses = await agent.handle_text(message)
#         logger.info(f"Bot responses: {responses}")
        
#         formatted_responses = []
#         for response in responses:
#             if isinstance(response, dict) and 'text' in response:
#                 formatted_responses.append({
#                     'recipient_id': sender_id,
#                     'text': response['text']
#                 })
#             elif isinstance(response, str):
#                 formatted_responses.append({
#                     'recipient_id': sender_id,
#                     'text': response
#                 })
        
#         response = jsonify(formatted_responses)
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Expose-Headers', 'Content-Type')
#         return response
        
#     except Exception as e:
#         logger.error(f"Error processing message: {e}")
#         return jsonify({"error": str(e)}), 500

# # Make sure event loop is properly handled for async operations
# def make_event_loop():
#     try:
#         return asyncio.get_event_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         return loop

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 10000))
#     logger.info(f"\nServer is running on http://0.0.0.0:{port}")
#     app.run(host='0.0.0.0', port=port)



# app.py (we will be back after)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import asyncio
# import os
# import logging

# # Configure logging and port
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# port = int(os.getenv('PORT', 10000))
# logger.info(f"Port configured as: {port}")

# app = Flask(__name__)

# # Configure CORS
# CORS(app, 
#      resources={
#          r"/*": {
#              "origins": [
#                  "http://localhost:8000",
#                  "http://127.0.0.1:8000",
#                  "http://localhost:5500",
#                  "http://127.0.0.1:5500",
#                  "https://drcmndr.github.io",
#                  "https://drcmndr.github.io/msubot-frontend",
#                  "*"
#              ],
#              "methods": ["GET", "POST", "OPTIONS"],
#              "allow_headers": ["Content-Type"],
#              "expose_headers": ["Content-Type"]
#          }
#      })

# # Initialize Rasa agent
# model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')
# try:
#     agent = Agent.load(model_path)
#     logger.info(f"Model loaded successfully from {model_path}")
# except Exception as e:
#     logger.error(f"Error loading model: {e}")
#     agent = None

# @app.route('/')
# def home():
#     return jsonify({
#         "status": "alive", 
#         "model_loaded": agent is not None,
#         "port": port  # Added port to health check response
#     })

# @app.route('/health')
# def health_check():
#     return jsonify({
#         "status": "healthy",
#         "port": port,
#         "model_loaded": agent is not None,
#         "model_path": model_path
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# async def webhook():
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
#         return response, 200

#     if not agent:
#         return jsonify({"error": "No model loaded"}), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         responses = await agent.handle_text(user_message)
#         response = jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])
        
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         return response

#     except Exception as e:
#         logger.error(f"Error processing message: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")  # Debug line for server start
#     logger.info(f"Server will be accessible at http://0.0.0.0:{port}")
#     app.run(host='0.0.0.0', port=port)






# app.py test

# from flask import Flask, jsonify
# import os
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# port = int(os.getenv('PORT', 10000))
# logger.info(f"Port configured as: {port}")

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return jsonify({"status": "alive", "port": port})

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)





# app.py test 2

# from flask import Flask, jsonify
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import os
# import logging
# from threading import Thread

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# port = int(os.getenv('PORT', 10000))
# logger.info(f"Port configured as: {port}")

# app = Flask(__name__)

# # Configure CORS
# CORS(app, 
#      resources={
#          r"/*": {
#              "origins": ["*"],
#              "methods": ["GET", "POST", "OPTIONS"],
#              "allow_headers": ["Content-Type"],
#              "expose_headers": ["Content-Type"]
#          }
#      })

# # Global agent variable
# agent = None

# def load_agent():
#     global agent
#     try:
#         model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')
#         agent = Agent.load(model_path)
#         logger.info(f"Model loaded successfully from {model_path}")
#     except Exception as e:
#         logger.error(f"Error loading model: {e}")

# # Start model loading in background
# Thread(target=load_agent, daemon=True).start()

# @app.route('/')
# def home():
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_loaded": agent is not None,
#         "model_loading": "in progress" if agent is None else "complete"
#     })

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)



# app.py test (progress)

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import os
# import logging
# from threading import Thread

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# port = int(os.getenv('PORT', 10000))
# logger.info(f"Port configured as: {port}")

# app = Flask(__name__)

# # Configure CORS for the base domain
# CORS(app, 
#      resources={
#          r"/*": {
#              "origins": ["https://drcmndr.github.io"],  # Changed this
#              "methods": ["GET", "POST", "OPTIONS"],
#              "allow_headers": ["Content-Type"],
#              "supports_credentials": False
#          }
#      })

# @app.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = 'https://drcmndr.github.io'  # Changed this
#     response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
#     return response

# # Global agent variable
# agent = None

# def load_agent():
#     global agent
#     try:
#         model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')
#         agent = Agent.load(model_path)
#         logger.info(f"Model loaded successfully from {model_path}")
#     except Exception as e:
#         logger.error(f"Error loading model: {e}")

# # Start model loading in background
# Thread(target=load_agent, daemon=True).start()

# @app.route('/')
# def home():
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_loaded": agent is not None
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     # Handle preflight request
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         response.headers.add('Access-Control-Allow-Origin', '*')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
#         return response

#     if not agent:
#         return jsonify({"error": "No model loaded"}), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         responses = app.ensure_sync(agent.handle_text)(user_message)
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])

#     except Exception as e:
#         logger.error(f"Error processing message: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)



# app.py 4


# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import os
# import logging
# from threading import Thread
# import time

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# port = int(os.getenv('PORT', 10000))
# logger.info(f"Port configured as: {port}")

# app = Flask(__name__)

# CORS(app, 
#      resources={
#          r"/*": {
#              "origins": ["https://drcmndr.github.io"],
#              "methods": ["GET", "POST", "OPTIONS"],
#              "allow_headers": ["Content-Type"],
#              "supports_credentials": False
#          }
#      })

# # Global agent variable
# agent = None
# agent_loading = False

# def load_agent():
#     global agent, agent_loading
#     agent_loading = True
#     try:
#         model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')
#         logger.info("Starting to load Rasa model...")
#         agent = Agent.load(model_path)
#         logger.info(f"Model loaded successfully from {model_path}")
#     except Exception as e:
#         logger.error(f"Error loading model: {e}")
#         agent = None
#     finally:
#         agent_loading = False

# # Start model loading in background
# Thread(target=load_agent, daemon=True).start()

# @app.route('/')
# def home():
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_loaded": agent is not None,
#         "model_loading": agent_loading
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     if request.method == 'OPTIONS':
#         return jsonify({'status': 'OK'})

#     # Check if model is still loading
#     if agent_loading:
#         return jsonify({
#             "error": "Model is still loading, please try again in a few seconds",
#             "status": "loading"
#         }), 503

#     # Check if model failed to load
#     if not agent:
#         try:
#             # Try to load the model again
#             Thread(target=load_agent, daemon=True).start()
#             return jsonify({
#                 "error": "Model not loaded, attempting to reload. Please try again in a few seconds",
#                 "status": "reloading"
#             }), 503
#         except Exception as e:
#             logger.error(f"Error reloading model: {e}")
#             return jsonify({"error": "Model loading failed"}), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         responses = app.ensure_sync(agent.handle_text)(user_message)
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])

#     except Exception as e:
#         logger.error(f"Error processing message: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)





from flask import Flask, jsonify, request
from flask_cors import CORS
from rasa.core.agent import Agent
import os
import logging
from threading import Thread
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

port = int(os.getenv('PORT', 10000))
logger.info(f"Port configured as: {port}")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io"]}})

# Global variables
agent = None
agent_loading = False
model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

def check_model_file():
    logger.info(f"Checking for model at: {model_path}")
    if os.path.exists(model_path):
        logger.info(f"Model file found at {model_path}")
        return True
    logger.error(f"Model file not found at {model_path}")
    return False

def load_agent():
    global agent, agent_loading
    agent_loading = True
    
    try:
        logger.info("Starting agent load process...")
        
        if not check_model_file():
            logger.error("Model file not found, cannot load agent")
            return

        logger.info("Attempting to load Rasa model...")
        loaded_agent = Agent.load(model_path)
        
        if loaded_agent:
            logger.info("Model loaded successfully!")
            agent = loaded_agent
        else:
            logger.error("Agent loaded but is None")
            
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}", exc_info=True)
        agent = None
    finally:
        agent_loading = False
        logger.info("Agent loading process completed")

@app.route('/')
def home():
    model_exists = check_model_file()
    return jsonify({
        "status": "alive",
        "port": port,
        "model_path": model_path,
        "model_exists": model_exists,
        "model_loaded": agent is not None,
        "model_loading": agent_loading
    })

@app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
def webhook():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'})

    if not check_model_file():
        return jsonify({"error": "Model file not found"}), 503

    if not agent and not agent_loading:
        logger.info("Agent not loaded, attempting to load...")
        Thread(target=load_agent, daemon=True).start()
        return jsonify({"error": "Model loading, please try again in a few seconds"}), 503

    if agent_loading:
        return jsonify({"error": "Model is still loading"}), 503

    if not agent:
        return jsonify({"error": "Model failed to load"}), 503

    try:
        data = request.json
        user_message = data.get('message')
        sender_id = data.get('sender', 'default')

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Processing message: {user_message}")
        responses = app.ensure_sync(agent.handle_text)(user_message)
        logger.info(f"Got responses: {responses}")
        
        return jsonify([{
            'recipient_id': sender_id,
            'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
        } for r in responses])

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Initial model load attempt
    Thread(target=load_agent, daemon=True).start()
    
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)