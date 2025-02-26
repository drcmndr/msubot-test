
# app.py

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from rasa.core.agent import Agent
# import os
# import logging
# from threading import Thread
# import time
# import sys
# import traceback

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# port = int(os.getenv('PORT', 10000))
# model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io"]}})

# # Global variables
# agent = None
# agent_loading = False
# load_error = None

# def load_agent():
#     global agent, agent_loading, load_error
#     agent_loading = True
#     load_error = None
    
#     try:
#         logger.info(f"Starting agent load process from {model_path}")
        
#         # Debug information
#         logger.info(f"Current working directory: {os.getcwd()}")
#         logger.info(f"Files in models directory: {os.listdir('models')}")
        
#         # Load the model
#         loaded_agent = Agent.load(model_path)
        
#         if loaded_agent:
#             logger.info("Model loaded successfully!")
#             agent = loaded_agent
#             load_error = None
#         else:
#             load_error = "Agent loaded as None"
#             logger.error(load_error)
            
#     except Exception as e:
#         load_error = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
#         logger.error(load_error)
#         agent = None
#     finally:
#         agent_loading = False
#         logger.info("Agent loading process completed")

# @app.route('/')
# def home():
#     global agent, agent_loading, load_error
    
#     # Force load if agent is None and not loading
#     if not agent and not agent_loading:
#         Thread(target=load_agent, daemon=True).start()
    
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_path": model_path,
#         "model_exists": os.path.exists(model_path),
#         "model_loaded": agent is not None,
#         "model_loading": agent_loading,
#         "last_error": load_error
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     global agent, agent_loading
    
#     if request.method == 'OPTIONS':
#         return jsonify({'status': 'OK'})

#     # Auto-load if not loaded
#     if not agent and not agent_loading:
#         Thread(target=load_agent, daemon=True).start()
#         return jsonify({
#             "error": "Model loading started, please retry in a few seconds",
#             "details": load_error
#         }), 503

#     if agent_loading:
#         return jsonify({
#             "error": "Model is still loading, please retry in a few seconds"
#         }), 503

#     if not agent:
#         return jsonify({
#             "error": "Model failed to load",
#             "details": load_error
#         }), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         logger.info(f"Processing message: {user_message}")
#         responses = app.ensure_sync(agent.handle_text)(user_message)
#         logger.info(f"Got responses: {responses}")
        
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])

#     except Exception as e:
#         error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
#         logger.error(error_details)
#         return jsonify({
#             "error": "Error processing message",
#             "details": error_details
#         }), 500

# if __name__ == '__main__':
#     # Initial model load attempt
#     Thread(target=load_agent, daemon=True).start()
    
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)



# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import os
# import logging
# import traceback
# from threading import Thread

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Get port from environment
# port = int(os.getenv('PORT', 10000))
# model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io", "http://localhost:5500"]}})

# # Global variables
# agent = None
# agent_loading = False
# load_error = None

# def load_agent():
#     global agent, agent_loading, load_error
#     agent_loading = True
#     load_error = None
    
#     try:
#         logger.info(f"Starting agent load process from {model_path}")
        
#         # Import Rasa only when needed to avoid startup issues
#         from rasa.core.agent import Agent
        
#         # Debug information
#         logger.info(f"Current working directory: {os.getcwd()}")
#         if os.path.exists('models'):
#             logger.info(f"Files in models directory: {os.listdir('models')}")
#         else:
#             logger.info("Models directory does not exist")
#             os.makedirs('models', exist_ok=True)
        
#         # Check if model exists
#         if not os.path.exists(model_path):
#             load_error = f"Model file not found at {model_path}"
#             logger.error(load_error)
#             agent = None
#             return
            
#         # Load the model
#         loaded_agent = Agent.load(model_path)
        
#         if loaded_agent:
#             logger.info("Model loaded successfully!")
#             agent = loaded_agent
#             load_error = None
#         else:
#             load_error = "Agent loaded as None"
#             logger.error(load_error)
            
#     except Exception as e:
#         load_error = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
#         logger.error(load_error)
#         agent = None
#     finally:
#         agent_loading = False
#         logger.info("Agent loading process completed")

# @app.route('/')
# def home():
#     global agent, agent_loading, load_error
    
#     # Display Python version and environment info
#     import sys
#     python_info = {
#         "version": sys.version,
#         "executable": sys.executable,
#         "platform": sys.platform
#     }
    
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_path": model_path,
#         "model_exists": os.path.exists(model_path),
#         "model_loaded": agent is not None,
#         "model_loading": agent_loading,
#         "last_error": load_error,
#         "python_info": python_info
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     global agent, agent_loading
    
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         return response
        
#     # Check if we should try to load the model
#     if not agent and not agent_loading:
#         Thread(target=load_agent, daemon=True).start()
#         return jsonify({
#             "error": "Model loading started, please retry in a few seconds",
#             "details": load_error
#         }), 503

#     if agent_loading:
#         return jsonify({
#             "error": "Model is still loading, please retry in a few seconds"
#         }), 503

#     if not agent:
#         return jsonify({
#             "error": "Model failed to load",
#             "details": load_error
#         }), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         logger.info(f"Processing message: {user_message}")
        
#         # Process the message
#         responses = app.ensure_sync(agent.handle_text)(user_message)
#         logger.info(f"Got responses: {responses}")
        
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])

#     except Exception as e:
#         error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
#         logger.error(error_details)
#         return jsonify({
#             "error": "Error processing message",
#             "details": error_details
#         }), 500

# # Start model loading in background when app starts
# Thread(target=load_agent, daemon=True).start()

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)






# app.py

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import os
# import logging
# import traceback
# from threading import Thread

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Get port from environment
# port = int(os.getenv('PORT', 10000))
# model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io", "http://localhost:5500"]}})

# # Global variables
# agent = None
# agent_loading = False
# load_error = None

# def load_agent():
#     global agent, agent_loading, load_error
#     agent_loading = True
#     load_error = None
    
#     try:
#         logger.info(f"Starting agent load process from {model_path}")
        
#         # Only import Rasa modules when needed
#         from rasa.core.agent import Agent
        
#         # Check if model exists
#         if not os.path.exists(model_path):
#             load_error = f"Model file not found at {model_path}"
#             logger.error(load_error)
#             agent = None
#             return
            
#         # Load the model without unnecessary components
#         loaded_agent = Agent.load(model_path, action_endpoint=None)
        
#         if loaded_agent:
#             logger.info("Model loaded successfully!")
#             agent = loaded_agent
#             load_error = None
#         else:
#             load_error = "Agent loaded as None"
#             logger.error(load_error)
            
#     except Exception as e:
#         load_error = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
#         logger.error(load_error)
#         agent = None
#     finally:
#         agent_loading = False
#         logger.info("Agent loading process completed")

# @app.route('/')
# def home():
#     global agent, agent_loading, load_error
    
#     # Display Python version and environment info
#     import sys
#     python_info = {
#         "version": sys.version,
#         "executable": sys.executable,
#         "platform": sys.platform
#     }
    
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_path": model_path,
#         "model_exists": os.path.exists(model_path),
#         "model_loaded": agent is not None,
#         "model_loading": agent_loading,
#         "last_error": load_error,
#         "python_info": python_info
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     global agent, agent_loading
    
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         return response
        
#     # Check if we should try to load the model
#     if not agent and not agent_loading:
#         Thread(target=load_agent, daemon=True).start()
#         return jsonify({
#             "error": "Model loading started, please retry in a few seconds",
#             "details": load_error
#         }), 503

#     if agent_loading:
#         return jsonify({
#             "error": "Model is still loading, please retry in a few seconds"
#         }), 503

#     if not agent:
#         return jsonify({
#             "error": "Model failed to load",
#             "details": load_error
#         }), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         logger.info(f"Processing message: {user_message}")
        
#         # Process the message
#         responses = app.ensure_sync(agent.handle_text)(user_message)
#         logger.info(f"Got responses: {responses}")
        
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])

#     except Exception as e:
#         error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
#         logger.error(error_details)
#         return jsonify({
#             "error": "Error processing message",
#             "details": error_details
#         }), 500

# # Start model loading in background when app starts
# Thread(target=load_agent, daemon=True).start()

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)



# simple app.py


# import os
# import subprocess
# import threading
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Get port from environment
# PORT = int(os.environ.get("PORT", 10000))
# MODEL_PATH = os.environ.get("RASA_MODEL", "models/20250219-213623-prompt-factor.tar.gz")

# # Global variable to store Rasa process
# rasa_process = None

# def start_rasa_server():
#     """Start Rasa server in a separate process"""
#     global rasa_process
    
#     # Define the command to start Rasa
#     cmd = [
#         "rasa", "run", 
#         "--enable-api",
#         f"--port={PORT+1}",  # Use PORT+1 for Rasa to avoid conflict with Flask
#         f"--model={MODEL_PATH}",
#         "--cors", "*"
#     ]
    
#     print(f"Starting Rasa server with command: {' '.join(cmd)}")
    
#     # Start Rasa as a subprocess
#     rasa_process = subprocess.Popen(cmd)
#     print("Rasa server started!")

# @app.route('/')
# def home():
#     return jsonify({
#         "status": "alive",
#         "message": "Flask server is running. Use /webhooks/rest/webhook for chatbot API."
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     if request.method == 'OPTIONS':
#         return jsonify({"status": "OK"})
        
#     # Forward the request to Rasa
#     import requests
    
#     rasa_url = f"http://localhost:{PORT+1}/webhooks/rest/webhook"
#     headers = {'Content-Type': 'application/json'}
    
#     try:
#         rasa_response = requests.post(
#             rasa_url,
#             json=request.json,
#             headers=headers
#         )
#         return jsonify(rasa_response.json())
#     except Exception as e:
#         return jsonify([{"text": f"Error: {str(e)}"}]), 500

# # Start Rasa when Flask starts
# threading.Thread(target=start_rasa_server, daemon=True).start()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=PORT)











# app.py tesesasr

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import os
# import logging
# import traceback
# from threading import Thread

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Get port from environment
# port = int(os.getenv('PORT', 10000))
# model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

# app = Flask(__name__)
# # Update CORS to allow your GitHub Pages domain and localhost for testing
# CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io", "http://localhost:5500", "*"]}})

# # Global variables
# agent = None
# agent_loading = False
# load_error = None

# def load_agent():
#     global agent, agent_loading, load_error
#     agent_loading = True
#     load_error = None
    
#     try:
#         logger.info(f"Starting agent load process from {model_path}")
        
#         # Only import Rasa modules when needed
#         from rasa.core.agent import Agent
        
#         # Check if model exists
#         if not os.path.exists(model_path):
#             load_error = f"Model file not found at {model_path}"
#             logger.error(load_error)
#             agent = None
#             return
            
#         # Load the model without unnecessary components
#         loaded_agent = Agent.load(model_path, action_endpoint=None)
        
#         if loaded_agent:
#             logger.info("Model loaded successfully!")
#             agent = loaded_agent
#             load_error = None
#         else:
#             load_error = "Agent loaded as None"
#             logger.error(load_error)
            
#     except Exception as e:
#         load_error = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
#         logger.error(load_error)
#         agent = None
#     finally:
#         agent_loading = False
#         logger.info("Agent loading process completed")

# @app.route('/')
# def home():
#     global agent, agent_loading, load_error
    
#     # Display Python version and environment info
#     import sys
#     python_info = {
#         "version": sys.version,
#         "executable": sys.executable,
#         "platform": sys.platform
#     }
    
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_path": model_path,
#         "model_exists": os.path.exists(model_path),
#         "model_loaded": agent is not None,
#         "model_loading": agent_loading,
#         "last_error": load_error,
#         "python_info": python_info
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     global agent, agent_loading
    
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         return response
        
#     # Check if we should try to load the model
#     if not agent and not agent_loading:
#         Thread(target=load_agent, daemon=True).start()
#         return jsonify({
#             "error": "Model loading started, please retry in a few seconds",
#             "details": load_error
#         }), 503

#     if agent_loading:
#         return jsonify({
#             "error": "Model is still loading, please retry in a few seconds"
#         }), 503

#     if not agent:
#         return jsonify({
#             "error": "Model failed to load",
#             "details": load_error
#         }), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         logger.info(f"Processing message: {user_message}")
        
#         # Process the message
#         responses = app.ensure_sync(agent.handle_text)(user_message)
#         logger.info(f"Got responses: {responses}")
        
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])

#     except Exception as e:
#         error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
#         logger.error(error_details)
#         return jsonify({
#             "error": "Error processing message",
#             "details": error_details
#         }), 500

# # Start model loading in background when app starts
# Thread(target=load_agent, daemon=True).start()

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)



# app.py (current working)

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import os
# import logging
# import traceback
# import subprocess
# import sys
# from threading import Thread

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Get port from environment
# port = int(os.getenv('PORT', 10000))
# model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io", "http://localhost:5500", "*"]}})

# # Global variables
# agent = None
# agent_loading = False
# load_error = None

# def install_spacy():
#     """Install spaCy and the English language model"""
#     logger.info("Attempting to install spaCy and language model...")
#     try:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
#         logger.info("SpaCy installed successfully")
        
#         subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
#         logger.info("SpaCy language model installed successfully")
#         return True
#     except Exception as e:
#         logger.error(f"Failed to install spaCy: {str(e)}")
#         return False

# def load_agent():
#     global agent, agent_loading, load_error
#     agent_loading = True
#     load_error = None
    
#     try:
#         logger.info(f"Starting agent load process from {model_path}")
        
#         # Check if spaCy is installed
#         try:
#             import spacy
#             logger.info("SpaCy is already installed")
#             try:
#                 nlp = spacy.load("en_core_web_sm")
#                 logger.info("SpaCy language model loaded successfully")
#             except OSError:
#                 logger.warning("SpaCy language model not found, installing...")
#                 if not install_spacy():
#                     load_error = "Failed to install SpaCy language model"
#                     agent = None
#                     return
#         except ImportError:
#             logger.warning("SpaCy not installed, installing...")
#             if not install_spacy():
#                 load_error = "Failed to install SpaCy"
#                 agent = None
#                 return
        
#         # Only import Rasa modules when needed
#         from rasa.core.agent import Agent
        
#         # Check if model exists
#         if not os.path.exists(model_path):
#             load_error = f"Model file not found at {model_path}"
#             logger.error(load_error)
#             agent = None
#             return
            
#         # Load the model without unnecessary components
#         loaded_agent = Agent.load(model_path, action_endpoint=None)
        
#         if loaded_agent:
#             logger.info("Model loaded successfully!")
#             agent = loaded_agent
#             load_error = None
#         else:
#             load_error = "Agent loaded as None"
#             logger.error(load_error)
            
#     except Exception as e:
#         load_error = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
#         logger.error(load_error)
#         agent = None
#     finally:
#         agent_loading = False
#         logger.info("Agent loading process completed")

# @app.route('/')
# def home():
#     global agent, agent_loading, load_error
    
#     # Display Python version and environment info
#     import sys
#     python_info = {
#         "version": sys.version,
#         "executable": sys.executable,
#         "platform": sys.platform
#     }
    
#     # Check if spaCy is installed
#     spacy_installed = False
#     spacy_model_installed = False
#     try:
#         import spacy
#         spacy_installed = True
#         try:
#             nlp = spacy.load("en_core_web_sm")
#             spacy_model_installed = True
#         except:
#             pass
#     except:
#         pass
    
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_path": model_path,
#         "model_exists": os.path.exists(model_path),
#         "model_loaded": agent is not None,
#         "model_loading": agent_loading,
#         "last_error": load_error,
#         "spacy_installed": spacy_installed,
#         "spacy_model_installed": spacy_model_installed,
#         "python_info": python_info
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     global agent, agent_loading
    
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         return response
        
#     # Check if we should try to load the model
#     if not agent and not agent_loading:
#         Thread(target=load_agent, daemon=True).start()
#         return jsonify({
#             "error": "Model loading started, please retry in a few seconds",
#             "details": load_error
#         }), 503

#     if agent_loading:
#         return jsonify({
#             "error": "Model is still loading, please retry in a few seconds"
#         }), 503

#     if not agent:
#         return jsonify({
#             "error": "Model failed to load",
#             "details": load_error
#         }), 503

#     try:
#         data = request.json
#         user_message = data.get('message')
#         sender_id = data.get('sender', 'default')

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         logger.info(f"Processing message: {user_message}")
        
#         # Process the message
#         responses = app.ensure_sync(agent.handle_text)(user_message)
#         logger.info(f"Got responses: {responses}")
        
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#         } for r in responses])

#     except Exception as e:
#         error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
#         logger.error(error_details)
#         return jsonify({
#             "error": "Error processing message",
#             "details": error_details
#         }), 500

# # Start model loading in background when app starts
# Thread(target=load_agent, daemon=True).start()

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)


# REVERT TO THIS VERSION AFTER

# # app.py version almost okay

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import os
# import logging
# import traceback
# import subprocess
# import sys
# import time
# import random
# from threading import Thread

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # Get port from environment
# port = int(os.getenv('PORT', 10000))
# model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io", "http://localhost:5500", "*"]}})

# # Global variables
# agent = None
# agent_loading = False
# load_error = None
# model_load_start_time = None
# is_first_load_attempt = True

# # Fallback responses when model is not ready
# FALLBACK_RESPONSES = [
#     "I'm still warming up my systems. Please try again in a moment.",
#     "My knowledge database is loading. Please try again shortly.",
#     "I'm getting ready to help you. Please try again in a few seconds.",
#     "I'm still initializing. Please try your question again soon.",
#     "My AI models are loading. Please try again in a moment."
# ]

# # Simple FAQ responses for common questions while model is loading
# SIMPLE_FAQ = {
#     "help": "I'm an AI assistant for MSU-IIT. I can answer questions about courses, campus information, and provide academic guidance. Please try again in a moment when my systems are fully loaded.",
#     "hello": "Hello! I'm A.L.A.B, your MSU-IIT virtual assistant. My advanced capabilities are still loading. Please try again in a moment.",
#     "hi": "Hi there! I'm A.L.A.B from MSU-IIT. My systems are still warming up. Please try again shortly.",
#     "about": "I'm A.L.A.B, the AI assistant for MSU-IIT. I'm designed to help with information about programs, admissions, and campus resources. My full capabilities will be available soon.",
#     "msu": "MSU-IIT (Mindanao State University - Iligan Institute of Technology) is a premier university in the Philippines. My complete knowledge base about MSU-IIT is still loading.",
#     "courses": "MSU-IIT offers a wide range of undergraduate and graduate programs. Please check back in a moment when my systems are fully loaded for detailed information.",
#     "contact": "For immediate assistance, you can contact MSU-IIT's main office. My complete contact directory is still loading."
# }

# def install_spacy():
#     """Install spaCy and the English language model"""
#     logger.info("Attempting to install spaCy and language model...")
#     try:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
#         logger.info("SpaCy installed successfully")
        
#         subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
#         logger.info("SpaCy language model installed successfully")
#         return True
#     except Exception as e:
#         logger.error(f"Failed to install spaCy: {str(e)}")
#         return False

# def load_agent():
#     global agent, agent_loading, load_error, model_load_start_time, is_first_load_attempt
#     agent_loading = True
#     load_error = None
#     model_load_start_time = time.time()
    
#     try:
#         logger.info(f"Starting agent load process from {model_path}")
        
#         # Check if spaCy is installed
#         try:
#             import spacy
#             logger.info("SpaCy is already installed")
#             try:
#                 nlp = spacy.load("en_core_web_sm")
#                 logger.info("SpaCy language model loaded successfully")
#             except OSError:
#                 logger.warning("SpaCy language model not found, installing...")
#                 if not install_spacy():
#                     load_error = "Failed to install SpaCy language model"
#                     agent = None
#                     return
#         except ImportError:
#             logger.warning("SpaCy not installed, installing...")
#             if not install_spacy():
#                 load_error = "Failed to install SpaCy"
#                 agent = None
#                 return
        
#         # Only import Rasa modules when needed
#         from rasa.core.agent import Agent
        
#         # Check if model exists
#         if not os.path.exists(model_path):
#             load_error = f"Model file not found at {model_path}"
#             logger.error(load_error)
#             agent = None
#             return
        
#         # Set lower memory usage for loading
#         os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
#         os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Disable GPU
        
#         logger.info("Loading model with reduced memory usage...")
            
#         # Load the model without unnecessary components
#         loaded_agent = Agent.load(model_path, action_endpoint=None)
        
#         if loaded_agent:
#             logger.info("Model loaded successfully!")
#             agent = loaded_agent
#             load_error = None
#         else:
#             load_error = "Agent loaded as None"
#             logger.error(load_error)
            
#     except Exception as e:
#         load_error = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
#         logger.error(load_error)
#         agent = None
#     finally:
#         agent_loading = False
#         is_first_load_attempt = False
#         loading_duration = time.time() - model_load_start_time
#         logger.info(f"Agent loading process completed in {loading_duration:.2f} seconds")

# def get_simple_response(message):
#     """Get a simple response for common questions when the model is loading"""
#     message_lower = message.lower()
    
#     for key, response in SIMPLE_FAQ.items():
#         if key in message_lower:
#             return response
    
#     return random.choice(FALLBACK_RESPONSES)

# @app.route('/')
# def home():
#     global agent, agent_loading, load_error, model_load_start_time
    
#     # Display Python version and environment info
#     import sys
#     python_info = {
#         "version": sys.version,
#         "executable": sys.executable,
#         "platform": sys.platform
#     }
    
#     # Check if spaCy is installed
#     spacy_installed = False
#     spacy_model_installed = False
#     try:
#         import spacy
#         spacy_installed = True
#         try:
#             nlp = spacy.load("en_core_web_sm")
#             spacy_model_installed = True
#         except:
#             pass
#     except:
#         pass
    
#     # Calculate loading time if applicable
#     loading_time = None
#     if model_load_start_time:
#         if agent_loading:
#             loading_time = time.time() - model_load_start_time
#         else:
#             loading_time = "completed"
    
#     return jsonify({
#         "status": "alive",
#         "port": port,
#         "model_path": model_path,
#         "model_exists": os.path.exists(model_path),
#         "model_loaded": agent is not None,
#         "model_loading": agent_loading,
#         "loading_time": loading_time,
#         "last_error": load_error,
#         "spacy_installed": spacy_installed,
#         "spacy_model_installed": spacy_model_installed,
#         "is_first_load_attempt": is_first_load_attempt,
#         "python_info": python_info
#     })

# @app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
# def webhook():
#     global agent, agent_loading, load_error
    
#     if request.method == 'OPTIONS':
#         response = jsonify({'status': 'OK'})
#         return response
        
#     # Get the user message
#     try:
#         data = request.json
#         user_message = data.get('message', '')
#         sender_id = data.get('sender', 'default')
        
#         if not user_message:
#             return jsonify([{
#                 "recipient_id": sender_id,
#                 "text": "I didn't receive any message. Could you please try again?"
#             }])
#     except Exception as e:
#         logger.error(f"Error parsing request: {str(e)}")
#         return jsonify([{
#             "recipient_id": "user",
#             "text": "I had trouble understanding your message. Could you try again?"
#         }])
    
#     # Check if we should try to load the model
#     if not agent and not agent_loading:
#         Thread(target=load_agent, daemon=True).start()
#         simple_response = get_simple_response(user_message)
#         return jsonify([{
#             "recipient_id": sender_id,
#             "text": simple_response
#         }])

#     # If model is still loading, provide a helpful response
#     if agent_loading:
#         loading_time = 0
#         if model_load_start_time:
#             loading_time = time.time() - model_load_start_time
            
#         simple_response = get_simple_response(user_message)
#         if loading_time > 60:
#             simple_response += f" (I've been loading for {int(loading_time)} seconds, thanks for your patience.)"
            
#         return jsonify([{
#             "recipient_id": sender_id,
#             "text": simple_response
#         }])

#     # If model failed to load, provide fallback response
#     if not agent:
#         if load_error:
#             logger.error(f"Using fallback response due to load error: {load_error}")
        
#         simple_response = get_simple_response(user_message)
#         return jsonify([{
#             "recipient_id": sender_id,
#             "text": simple_response + " (My main AI system is still initializing.)"
#         }])

#     # Process with the loaded model
#     try:
#         logger.info(f"Processing message: {user_message}")
        
#         # Process the message with timeout protection
#         try:
#             # Use a shorter timeout to avoid worker timeout issues
#             import threading
#             response_received = False
#             responses = []
            
#             def process_message():
#                 nonlocal responses, response_received
#                 try:
#                     responses = app.ensure_sync(agent.handle_text)(user_message)
#                     response_received = True
#                 except Exception as e:
#                     logger.error(f"Error in model processing: {str(e)}")
            
#             # Start message processing in a thread
#             process_thread = threading.Thread(target=process_message)
#             process_thread.daemon = True
#             process_thread.start()
            
#             # Wait for response with timeout
#             process_thread.join(timeout=25)  # 25 second timeout - must be less than worker timeout
            
#             if not response_received:
#                 logger.warning(f"Model response timed out for: {user_message}")
#                 return jsonify([{
#                     'recipient_id': sender_id,
#                     'text': "I'm taking too long to process your question. Could you try a shorter or simpler query?"
#                 }])
            
#             logger.info(f"Got responses: {responses}")
            
#             return jsonify([{
#                 'recipient_id': sender_id,
#                 'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
#             } for r in responses])
            
#         except Exception as timeout_error:
#             logger.error(f"Error with message processing: {str(timeout_error)}")
#             return jsonify([{
#                 'recipient_id': sender_id,
#                 'text': "I encountered an issue processing your request. Could you try again with different wording?"
#             }])

#     except Exception as e:
#         error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
#         logger.error(error_details)
#         return jsonify([{
#             'recipient_id': sender_id,
#             'text': "I'm having trouble understanding your request. Please try again with a different question."
#         }])

# # Start model loading in background when app starts
# Thread(target=load_agent, daemon=True).start()

# if __name__ == '__main__':
#     logger.info(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port)















from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
import traceback
import subprocess
import sys
import time
import random
import threading
import gc  # Garbage collection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get port from environment
port = int(os.getenv('PORT', 10000))
model_path = os.getenv('RASA_MODEL', 'models/20250219-213623-prompt-factor.tar.gz')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global variables
agent = None
agent_loading = False
load_error = None
model_load_start_time = None
is_first_load_attempt = True
loading_lock = threading.Lock()

# Fallback responses when model is not ready
FALLBACK_RESPONSES = [
    "I'm still warming up my systems. Please try again in a moment.",
    "My knowledge database is loading. Please try again shortly.",
    "I'm getting ready to help you. Please try again in a few seconds.",
    "I'm still initializing. Please try your question again soon.",
    "My AI models are loading. Please try again in a moment."
]

# Simple FAQ responses for common questions while model is loading
SIMPLE_FAQ = {
    "help": "I'm an AI assistant for MSU-IIT. I can answer questions about courses, campus information, and provide academic guidance. Please try again in a moment when my systems are fully loaded.",
    "hello": "Hello! I'm A.L.A.B, your MSU-IIT virtual assistant. My advanced capabilities are still loading. Please try again in a moment.",
    "hi": "Hi there! I'm A.L.A.B from MSU-IIT. My systems are still warming up. Please try again shortly.",
    "about": "I'm A.L.A.B, the AI assistant for MSU-IIT. I'm designed to help with information about programs, admissions, and campus resources. My full capabilities will be available soon.",
    "msu": "MSU-IIT (Mindanao State University - Iligan Institute of Technology) is a premier university in the Philippines. My complete knowledge base about MSU-IIT is still loading.",
    "courses": "MSU-IIT offers a wide range of undergraduate and graduate programs. Please check back in a moment when my systems are fully loaded for detailed information.",
    "contact": "For immediate assistance, you can contact MSU-IIT's main office. My complete contact directory is still loading."
}

def get_simple_response(message):
    """Get a simple response for common questions when the model is loading"""
    message_lower = message.lower()
    
    for key, response in SIMPLE_FAQ.items():
        if key in message_lower:
            return response
    
    return random.choice(FALLBACK_RESPONSES)

def load_agent_with_timeout(timeout=540):  # 9 minutes timeout to stay under worker timeout
    """Load agent with a timeout to avoid worker timeout issues"""
    global agent, agent_loading, load_error, model_load_start_time, is_first_load_attempt
    
    # Use lock to prevent multiple loading attempts
    if not loading_lock.acquire(blocking=False):
        logger.info("Another thread is already loading the model")
        return
    
    try:
        agent_loading = True
        load_error = None
        model_load_start_time = time.time()
        
        logger.info(f"Starting agent load process from {model_path}")

        # Set memory optimization environment variables
        os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'       # Disable GPU
        os.environ['OMP_NUM_THREADS'] = '1'             # Limit OpenMP threads
        os.environ['MKL_NUM_THREADS'] = '1'             # Limit MKL threads
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Disable tokenizer parallelism
        
        # Force garbage collection
        gc.collect()
        
        # Check if model exists
        if not os.path.exists(model_path):
            load_error = f"Model file not found at {model_path}"
            logger.error(load_error)
            return
            
        # Create a thread to load the model
        def load_model_thread():
            global agent, load_error
            try:
                # Only import Rasa modules when needed to save memory
                from rasa.core.agent import Agent
                logger.info("Rasa modules imported, loading model...")
                
                # Load the model with minimal components
                loaded_agent = Agent.load(
                    model_path, 
                    action_endpoint=None,
                )
                
                if loaded_agent:
                    logger.info("Model loaded successfully!")
                    agent = loaded_agent
                    load_error = None
                else:
                    load_error = "Agent loaded as None"
                    logger.error(load_error)
                    
            except Exception as e:
                load_error = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
                logger.error(load_error)
        
        # Start loading thread
        loading_thread = threading.Thread(target=load_model_thread)
        loading_thread.daemon = True
        loading_thread.start()
        
        # Wait for thread with timeout
        loading_thread.join(timeout=timeout)
        
        if loading_thread.is_alive():
            load_error = f"Model loading timed out after {timeout} seconds"
            logger.error(load_error)
            
            # We'll continue with no model but avoid killing the thread
            # It might finish eventually, but we won't block the server
            
    except Exception as e:
        load_error = f"Error in load_agent_with_timeout: {str(e)}\n{traceback.format_exc()}"
        logger.error(load_error)
    finally:
        # Even if we timed out, we still mark loading as complete to unblock requests
        agent_loading = False
        is_first_load_attempt = False
        loading_duration = time.time() - model_load_start_time
        logger.info(f"Agent loading process completed in {loading_duration:.2f} seconds")
        loading_lock.release()
        
        # Force garbage collection again
        gc.collect()

def simple_response_mode():
    """Check if we should use simple response mode instead of the full model"""
    global agent, agent_loading, load_error, model_load_start_time
    
    # Use simple mode if:
    # 1. Model is still loading
    if agent_loading:
        return True
        
    # 2. Model failed to load
    if not agent and load_error:
        return True
        
    # 3. Model is taking too long to load (over 10 minutes)
    if agent_loading and model_load_start_time and (time.time() - model_load_start_time > 600):
        return True
        
    return False

@app.route('/')
def home():
    global agent, agent_loading, load_error, model_load_start_time
    
    # Display Python version and environment info
    import sys
    python_info = {
        "version": sys.version,
        "executable": sys.executable,
        "platform": sys.platform
    }
    
    # Check if spaCy is installed
    spacy_installed = False
    spacy_model_installed = False
    try:
        import spacy
        spacy_installed = True
        try:
            nlp = spacy.load("en_core_web_sm")
            spacy_model_installed = True
        except:
            pass
    except:
        pass
    
    # Calculate loading time if applicable
    loading_time = None
    if model_load_start_time:
        if agent_loading:
            loading_time = time.time() - model_load_start_time
        else:
            loading_time = time.time() - model_load_start_time

    # Memory usage information
    memory_info = {}
    try:
        import psutil
        process = psutil.Process(os.getpid())
        memory_info = {
            "rss_mb": process.memory_info().rss / 1024 / 1024,
            "vms_mb": process.memory_info().vms / 1024 / 1024,
            "percent": process.memory_percent()
        }
    except:
        memory_info = {"error": "psutil not available"}
    
    return jsonify({
        "status": "alive",
        "port": port,
        "model_path": model_path,
        "model_exists": os.path.exists(model_path),
        "model_loaded": agent is not None,
        "model_loading": agent_loading,
        "loading_time": loading_time,
        "last_error": load_error,
        "spacy_installed": spacy_installed,
        "spacy_model_installed": spacy_model_installed,
        "is_first_load_attempt": is_first_load_attempt,
        "simple_response_mode": simple_response_mode(),
        "memory_info": memory_info,
        "python_info": python_info
    })

@app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
def webhook():
    global agent, agent_loading, load_error, model_load_start_time
    
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        return response
        
    # Get the user message
    try:
        data = request.json
        user_message = data.get('message', '')
        sender_id = data.get('sender', 'default')
        
        if not user_message:
            return jsonify([{
                "recipient_id": sender_id,
                "text": "I didn't receive any message. Could you please try again?"
            }])
    except Exception as e:
        logger.error(f"Error parsing request: {str(e)}")
        return jsonify([{
            "recipient_id": "user",
            "text": "I had trouble understanding your message. Could you try again?"
        }])
    
    # Check if we should try to load the model
    if not agent and not agent_loading and not load_error:
        # Start loading in background
        thread = threading.Thread(target=load_agent_with_timeout)
        thread.daemon = True
        thread.start()
        
        # Return a simple response meanwhile
        simple_response = get_simple_response(user_message)
        return jsonify([{
            "recipient_id": sender_id,
            "text": simple_response
        }])

    # If we're in simple response mode, return a simple response
    if simple_response_mode():
        logger.info(f"Using simple response mode for: {user_message}")
        simple_response = get_simple_response(user_message)
        
        # Add context about loading status if applicable
        if agent_loading and model_load_start_time:
            loading_time = time.time() - model_load_start_time
            if loading_time > 60:
                simple_response += f" (I've been loading for {int(loading_time)} seconds, thanks for your patience.)"
        elif load_error:
            simple_response += " (My AI system is currently in basic mode.)"
            
        return jsonify([{
            "recipient_id": sender_id,
            "text": simple_response
        }])

    # Process with the loaded model
    try:
        logger.info(f"Processing message with Rasa: {user_message}")
        
        # Process the message with timeout protection
        response_received = False
        responses = []
        
        def process_message():
            nonlocal responses, response_received
            try:
                responses = app.ensure_sync(agent.handle_text)(user_message)
                response_received = True
            except Exception as e:
                logger.error(f"Error in model processing: {str(e)}\n{traceback.format_exc()}")
        
        # Start message processing in a thread
        process_thread = threading.Thread(target=process_message)
        process_thread.daemon = True
        process_thread.start()
        
        # Wait for response with timeout (15 seconds should be plenty for inference)
        process_thread.join(timeout=15)
        
        if not response_received:
            logger.warning(f"Model response timed out for: {user_message}")
            return jsonify([{
                'recipient_id': sender_id,
                'text': "I'm taking too long to process your question. Could you try a shorter or simpler query?"
            }])
        
        if not responses:
            logger.warning(f"Empty response from model for: {user_message}")
            return jsonify([{
                'recipient_id': sender_id,
                'text': "I understood your question, but I'm not sure how to respond. Could you try asking in a different way?"
            }])
        
        logger.info(f"Got responses from Rasa: {responses}")
        
        return jsonify([{
            'recipient_id': sender_id,
            'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
        } for r in responses])

    except Exception as e:
        error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_details)
        return jsonify([{
            'recipient_id': sender_id,
            'text': "I'm having trouble understanding your request. Please try again with a different question."
        }])

# Start model loading in background when app starts
thread = threading.Thread(target=load_agent_with_timeout)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)
