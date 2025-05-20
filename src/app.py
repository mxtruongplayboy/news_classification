from flask import Flask, render_template, request, jsonify
from model_manager import ModelManager
import os
import logging
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_app.log'))
    ]
)
logger = logging.getLogger('flask_app')

# Create a global model_manager
model_manager = None

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    
    # Initialize the ModelManager if not already initialized
    global model_manager
    if model_manager is None:
        logger.info("Initializing ModelManager...")
        model_manager = ModelManager()
        logger.info("ModelManager initialized successfully.")
    
    @app.route('/')
    def index():
        logger.info("Index page accessed")
        return render_template('index.html')
    
    @app.route('/classify', methods=['POST'])
    def classify():
        # Generate a unique request ID
        request_id = str(uuid.uuid4())[:8]
        logger.info(f"[{request_id}] Classification request received")
        
        # Get form data
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        content = request.form.get('content', '')
        model_type = request.form.get('modelType', 'logistic_regression_model')
        
        # Log request details
        logger.info(f"[{request_id}] Model type: {model_type}")
        logger.info(f"[{request_id}] Title length: {len(title)} characters")
        logger.info(f"[{request_id}] Description length: {len(description)} characters")
        logger.info(f"[{request_id}] Content length: {len(content)} characters")
        
        # Determine if we're using machine learning or deep learning models
        if model_type in ['logistic_regression_model', 'naive_bayes_model']:
            # Use machine learning models
            logger.info(f"[{request_id}] Using machine learning model: {model_type}")
            result = model_manager.predict_with_machine_learning(title, description, content, model_type)
        else:
            # Use deep learning models
            logger.info(f"[{request_id}] Using deep learning model: {model_type}")
            result = model_manager.predict_with_deep_learning(title, description, content, model_type)
        
        # Check for errors
        if 'error' in result:
            logger.error(f"[{request_id}] Error during classification: {result['error']}")
            return jsonify({
                "error": result['error'],
                "predicted_topic": "Unknown",
                "model_info": {
                    "type": "Unknown",
                    "name": "Error",
                    "accuracy": "0%"
                },
                "probabilities": []
            })
        
        # Log successful classification
        logger.info(f"[{request_id}] Classification successful. Predicted topic: {result['predicted_topic']}")
        logger.info(f"[{request_id}] Classification completed with model: {result['model_info']['name']}")
        
        return jsonify(result)
    
    return app

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app = create_app()
    logger.info("Flask application created, starting server...")
    app.run(debug=False)  # Set debug to False to avoid reloading issues 