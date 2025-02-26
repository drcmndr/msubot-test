
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

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
import traceback
import subprocess
import sys
from threading import Thread

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
CORS(app, resources={r"/*": {"origins": ["https://drcmndr.github.io", "http://localhost:5500", "*"]}})

# Global variables
agent = None
agent_loading = False
load_error = None

def install_spacy():
    """Install spaCy and the English language model"""
    logger.info("Attempting to install spaCy and language model...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
        logger.info("SpaCy installed successfully")
        
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        logger.info("SpaCy language model installed successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to install spaCy: {str(e)}")
        return False

def load_agent():
    global agent, agent_loading, load_error
    agent_loading = True
    load_error = None
    
    try:
        logger.info(f"Starting agent load process from {model_path}")
        
        # Check if spaCy is installed
        try:
            import spacy
            logger.info("SpaCy is already installed")
            try:
                nlp = spacy.load("en_core_web_sm")
                logger.info("SpaCy language model loaded successfully")
            except OSError:
                logger.warning("SpaCy language model not found, installing...")
                if not install_spacy():
                    load_error = "Failed to install SpaCy language model"
                    agent = None
                    return
        except ImportError:
            logger.warning("SpaCy not installed, installing...")
            if not install_spacy():
                load_error = "Failed to install SpaCy"
                agent = None
                return
        
        # Only import Rasa modules when needed
        from rasa.core.agent import Agent
        
        # Check if model exists
        if not os.path.exists(model_path):
            load_error = f"Model file not found at {model_path}"
            logger.error(load_error)
            agent = None
            return
            
        # Load the model without unnecessary components
        loaded_agent = Agent.load(model_path, action_endpoint=None)
        
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
        agent = None
    finally:
        agent_loading = False
        logger.info("Agent loading process completed")

@app.route('/')
def home():
    global agent, agent_loading, load_error
    
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
    
    return jsonify({
        "status": "alive",
        "port": port,
        "model_path": model_path,
        "model_exists": os.path.exists(model_path),
        "model_loaded": agent is not None,
        "model_loading": agent_loading,
        "last_error": load_error,
        "spacy_installed": spacy_installed,
        "spacy_model_installed": spacy_model_installed,
        "python_info": python_info
    })

@app.route('/webhooks/rest/webhook', methods=['POST', 'OPTIONS'])
def webhook():
    global agent, agent_loading
    
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        return response
        
    # Check if we should try to load the model
    if not agent and not agent_loading:
        Thread(target=load_agent, daemon=True).start()
        return jsonify({
            "error": "Model loading started, please retry in a few seconds",
            "details": load_error
        }), 503

    if agent_loading:
        return jsonify({
            "error": "Model is still loading, please retry in a few seconds"
        }), 503

    if not agent:
        return jsonify({
            "error": "Model failed to load",
            "details": load_error
        }), 503

    try:
        data = request.json
        user_message = data.get('message')
        sender_id = data.get('sender', 'default')

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Processing message: {user_message}")
        
        # Process the message
        responses = app.ensure_sync(agent.handle_text)(user_message)
        logger.info(f"Got responses: {responses}")
        
        return jsonify([{
            'recipient_id': sender_id,
            'text': r.get('text', str(r)) if isinstance(r, dict) else str(r)
        } for r in responses])

    except Exception as e:
        error_details = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_details)
        return jsonify({
            "error": "Error processing message",
            "details": error_details
        }), 500

# Start model loading in background when app starts
Thread(target=load_agent, daemon=True).start()

if __name__ == '__main__':
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)