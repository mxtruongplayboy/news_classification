import os
import joblib
import pickle
import numpy as np
import time
import logging
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from text_cleaner import TextCleaner
import sys
from pathlib import Path

LOG_PATH = os.path.join(os.path.dirname(__file__), 'classification.log')

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Tạo File Handler với encoding UTF-8
file_handler = logging.FileHandler(Path(LOG_PATH), encoding='utf-8')
file_handler.setFormatter(log_formatter)

# Tạo Stream Handler (ghi ra console)
stream_handler = logging.StreamHandler(sys.stdout) # Hoặc sys.stderr
stream_handler.setFormatter(log_formatter)

# Lấy logger gốc và cấu hình handlers
logger = logging.getLogger() # Lấy root logger
logger.setLevel(logging.INFO)
logger.handlers.clear() # Xóa các handler mặc định nếu có
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
class ModelManager:
    def __init__(self):
        # Define base directories
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.MODEL_DIR = os.path.join(self.BASE_DIR, 'models')
        
        # Initialize paths for text cleaning
        self.stopwords_file = os.path.join(self.BASE_DIR, 'crawl', 'stopwords.txt')
        self.abbreviations_file = os.path.join(self.BASE_DIR, 'crawl', 'acronym.txt')
        self.vncorenlp_model_dir = os.path.join(self.BASE_DIR, 'vncorenlp')
        
        # Initialize paths for machine learning models
        self.tfidf_vectorizer_path = os.path.join(self.MODEL_DIR, 'tfidf_vectorizer.joblib')
        self.nb_model_path = os.path.join(self.MODEL_DIR, 'naive_bayes_model.joblib')
        self.lr_model_path = os.path.join(self.MODEL_DIR, 'logistic_regression_model.joblib')
        
        # Initialize paths for deep learning models
        self.tokenizer_path = os.path.join(self.MODEL_DIR, 'tokenizer.pkl')
        self.label_encoder_path = os.path.join(self.MODEL_DIR, 'label_encoder.pkl')
        self.max_len_path = os.path.join(self.MODEL_DIR, 'max_len.pkl')
        self.bigru_model_path = os.path.join(self.MODEL_DIR, 'bigru_model.keras')
        self.bilstm_model_path = os.path.join(self.MODEL_DIR, 'bilstm_model.keras')
        
        # Initialize model components
        self.cleaner = None
        
        # Machine learning components
        self.tfidf_vectorizer = None
        self.nb_model = None
        self.lr_model = None
        
        # Deep learning components
        self.tokenizer = None
        self.label_encoder = None
        self.max_len = None
        self.bigru_model = None
        self.bilstm_model = None
        
        # Load models
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize all models and components"""
        logger.info("Initializing models...")
        
        # Initialize text cleaner
        try:
            logger.info("Initializing TextCleaner...")
            self.cleaner = TextCleaner(self.stopwords_file, self.abbreviations_file, self.vncorenlp_model_dir)
            logger.info("TextCleaner initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing TextCleaner: {e}")
        
        # Load machine learning models
        try:
            logger.info("Loading TF-IDF Vectorizer...")
            if os.path.exists(self.tfidf_vectorizer_path):
                self.tfidf_vectorizer = joblib.load(self.tfidf_vectorizer_path)
                logger.info(f"TF-IDF Vectorizer loaded from: {self.tfidf_vectorizer_path}")
            else:
                logger.warning(f"TF-IDF Vectorizer file not found at: {self.tfidf_vectorizer_path}")
        except Exception as e:
            logger.error(f"Error loading TF-IDF Vectorizer: {e}")
        
        try:
            logger.info("Loading Naive Bayes model...")
            if os.path.exists(self.nb_model_path):
                self.nb_model = joblib.load(self.nb_model_path)
                logger.info(f"Naive Bayes model loaded from: {self.nb_model_path}")
            else:
                logger.warning(f"Naive Bayes model file not found at: {self.nb_model_path}")
        except Exception as e:
            logger.error(f"Error loading Naive Bayes model: {e}")
        
        try:
            logger.info("Loading Logistic Regression model...")
            if os.path.exists(self.lr_model_path):
                self.lr_model = joblib.load(self.lr_model_path)
                logger.info(f"Logistic Regression model loaded from: {self.lr_model_path}")
            else:
                logger.warning(f"Logistic Regression model file not found at: {self.lr_model_path}")
        except Exception as e:
            logger.error(f"Error loading Logistic Regression model: {e}")
        
        # Load deep learning models
        try:
            logger.info("Loading tokenizer...")
            if os.path.exists(self.tokenizer_path):
                with open(self.tokenizer_path, 'rb') as handle:
                    self.tokenizer = pickle.load(handle)
                logger.info(f"Tokenizer loaded from: {self.tokenizer_path}")
            else:
                logger.warning(f"Tokenizer file not found at: {self.tokenizer_path}")
        except Exception as e:
            logger.error(f"Error loading tokenizer: {e}")
        
        try:
            logger.info("Loading label encoder...")
            if os.path.exists(self.label_encoder_path):
                with open(self.label_encoder_path, 'rb') as handle:
                    self.label_encoder = pickle.load(handle)
                logger.info(f"Label encoder loaded from: {self.label_encoder_path}")
            else:
                logger.warning(f"Label encoder file not found at: {self.label_encoder_path}")
        except Exception as e:
            logger.error(f"Error loading label encoder: {e}")
        
        try:
            logger.info("Loading max_len...")
            if os.path.exists(self.max_len_path):
                with open(self.max_len_path, 'rb') as handle:
                    self.max_len = pickle.load(handle)
                logger.info(f"Max length loaded: {self.max_len} from {self.max_len_path}")
            else:
                logger.warning(f"Max length file not found at: {self.max_len_path}")
        except Exception as e:
            logger.error(f"Error loading max_len: {e}")
        
        try:
            logger.info("Loading BiGRU model...")
            if os.path.exists(self.bigru_model_path):
                self.bigru_model = load_model(self.bigru_model_path)
                logger.info(f"BiGRU model loaded from: {self.bigru_model_path}")
            else:
                logger.warning(f"BiGRU model file not found at: {self.bigru_model_path}")
        except Exception as e:
            logger.error(f"Error loading BiGRU model: {e}")
        
        try:
            logger.info("Loading BiLSTM model...")
            if os.path.exists(self.bilstm_model_path):
                self.bilstm_model = load_model(self.bilstm_model_path)
                logger.info(f"BiLSTM model loaded from: {self.bilstm_model_path}")
            else:
                logger.warning(f"BiLSTM model file not found at: {self.bilstm_model_path}")
        except Exception as e:
            logger.error(f"Error loading BiLSTM model: {e}")
        
        logger.info("Model initialization complete.")
    
    def clean_text(self, title, description, content):
        """Clean the input text using TextCleaner"""
        if self.cleaner is None:
            logger.error("TextCleaner not initialized. Cannot clean text.")
            return None, None, None, None
        
        try:
            logger.info("Cleaning input text...")
            title_cleaned, description_cleaned, content_cleaned = self.cleaner.process_text(title, description, content)
            combined_text = title_cleaned + " " + description_cleaned + " " + content_cleaned
            logger.info(f"Text cleaned successfully. Combined length: {len(combined_text)} characters")
            return title_cleaned, description_cleaned, content_cleaned, combined_text
        except Exception as e:
            logger.error(f"Error cleaning text: {e}")
            return None, None, None, None
    
    def predict_with_machine_learning(self, title, description, content, model_type="logistic_regression_model"):
        """Predict using machine learning models"""
        start_time = time.time()
        logger.info(f"Starting prediction with {model_type}...")
        
        # Log input text summary
        title_summary = title[:50] + "..." if len(title) > 50 else title
        logger.info(f"Input title: {title_summary}")
        
        # Clean the text
        _, _, _, combined_text = self.clean_text(title, description, content)
        if combined_text is None:
            logger.error("Failed to clean text for prediction")
            return {"error": "Error cleaning text"}
        
        # Check if required components are loaded
        if self.tfidf_vectorizer is None:
            logger.error("TF-IDF Vectorizer not loaded")
            return {"error": "TF-IDF Vectorizer not loaded"}
        
        # Choose model based on model_type
        if model_type == "naive_bayes_model":
            if self.nb_model is None:
                logger.error("Naive Bayes model not loaded")
                return {"error": "Naive Bayes model not loaded"}
            model = self.nb_model
            model_name = "Naive Bayes"
        else:  # Default to logistic regression
            if self.lr_model is None:
                logger.error("Logistic Regression model not loaded")
                return {"error": "Logistic Regression model not loaded"}
            model = self.lr_model
            model_name = "Logistic Regression"
        
        logger.info(f"Using {model_name} model for prediction")
        
        # Vectorize the text
        try:
            text_tfidf = self.tfidf_vectorizer.transform([combined_text])
            logger.info(f"Text vectorized successfully. Shape: {text_tfidf.shape}")
        except Exception as e:
            logger.error(f"Error vectorizing text: {e}")
            return {"error": f"Error vectorizing text: {e}"}
        
        # Predict
        try:
            prediction = model.predict(text_tfidf)[0]
            logger.info(f"Prediction result: {prediction}")
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return {"error": f"Error during prediction: {e}"}
        
        # Get probabilities
        result = {}
        if hasattr(model, "predict_proba") and hasattr(model, "classes_"):
            try:
                prediction_proba = model.predict_proba(text_tfidf)[0]
                
                # Format the response
                probabilities = []
                for i, topic_class in enumerate(model.classes_):
                    probabilities.append({
                        "topic": topic_class,
                        "probability": float(prediction_proba[i])
                    })
                
                # Sort probabilities in descending order
                probabilities.sort(key=lambda x: x["probability"], reverse=True)
                
                # Get accuracy from highest probability
                highest_probability = probabilities[0]["probability"] if probabilities else 0
                accuracy = f"{highest_probability * 100:.2f}%"
                
                # Log top 5 predictions
                logger.info("Top 5 predictions:")
                for i, prob in enumerate(probabilities[:5]):
                    logger.info(f"  {i+1}. {prob['topic']}: {prob['probability']:.4f}")
                
                result = {
                    "predicted_topic": prediction,
                    "model_info": {
                        "type": "Machine Learning",
                        "name": model_name,
                        "accuracy": accuracy
                    },
                    "probabilities": probabilities
                }
            except Exception as e:
                logger.error(f"Error getting prediction probabilities: {e}")
                result = {
                    "predicted_topic": prediction,
                    "model_info": {
                        "type": "Machine Learning",
                        "name": model_name,
                        "accuracy": accuracy
                    },
                    "probabilities": []
                }
        else:
            logger.warning("Model does not support probability estimation")
            result = {
                "predicted_topic": prediction,
                "model_info": {
                    "type": "Machine Learning",
                    "name": model_name,
                    "accuracy": accuracy
                },
                "probabilities": []
            }
        
        elapsed_time = time.time() - start_time
        logger.info(f"Prediction completed in {elapsed_time:.2f} seconds")
        return result
    
    def predict_with_deep_learning(self, title, description, content, model_type="bilstm_model"):
        """Predict using deep learning models"""
        start_time = time.time()
        logger.info(f"Starting prediction with {model_type}...")
        
        # Log input text summary
        title_summary = title[:50] + "..." if len(title) > 50 else title
        logger.info(f"Input title: {title_summary}")
        
        # Clean the text
        _, _, _, combined_text = self.clean_text(title, description, content)
        if combined_text is None:
            logger.error("Failed to clean text for prediction")
            return {"error": "Error cleaning text"}
        
        # Check if required components are loaded
        if self.tokenizer is None:
            logger.error("Tokenizer not loaded")
            return {"error": "Tokenizer not loaded"}
        if self.label_encoder is None:
            logger.error("Label encoder not loaded")
            return {"error": "Label encoder not loaded"}
        if self.max_len is None:
            logger.error("Max length not loaded")
            return {"error": "Max length not loaded"}
        
        # Choose model based on model_type
        if model_type == "bigru_model":
            if self.bigru_model is None:
                logger.error("BiGRU model not loaded")
                return {"error": "BiGRU model not loaded"}
            model = self.bigru_model
            model_name = "BiGRU"
        else:  # Default to BiLSTM
            if self.bilstm_model is None:
                logger.error("BiLSTM model not loaded")
                return {"error": "BiLSTM model not loaded"}
            model = self.bilstm_model
            model_name = "BiLSTM"
        
        logger.info(f"Using {model_name} model for prediction")
        
        # Tokenize and Pad
        try:
            sequence = self.tokenizer.texts_to_sequences([combined_text])
            padded_sequence = pad_sequences(sequence, maxlen=self.max_len, padding='post', truncating='post')
            logger.info(f"Text tokenized and padded successfully. Shape: {padded_sequence.shape}")
        except Exception as e:
            logger.error(f"Error in tokenization or padding: {e}")
            return {"error": f"Error in tokenization or padding: {e}"}
        
        # Predict
        try:
            prediction_proba = model.predict(padded_sequence)[0]
            predicted_class_index = np.argmax(prediction_proba)
            predicted_class_label = self.label_encoder.inverse_transform([predicted_class_index])[0]
            prediction_accuracy = float(prediction_proba[predicted_class_index])
            logger.info(f"Prediction result: {predicted_class_label} with accuracy: {prediction_accuracy:.4f}")
            
            # Format the response
            probabilities = []
            if hasattr(self.label_encoder, 'classes_'):
                for i, topic_class_name in enumerate(self.label_encoder.classes_):
                    probabilities.append({
                        "topic": topic_class_name,
                        "probability": float(prediction_proba[i])
                    })
                
                # Sort probabilities in descending order
                probabilities.sort(key=lambda x: x["probability"], reverse=True)
                
                # Log top 5 predictions
                logger.info("Top 5 predictions:")
                for i, prob in enumerate(probabilities[:5]):
                    logger.info(f"  {i+1}. {prob['topic']}: {prob['probability']:.4f}")
            
            result = {
                "predicted_topic": predicted_class_label,
                "model_info": {
                    "type": "Deep Learning",
                    "name": model_name,
                    "accuracy": f"{prediction_accuracy:.2%}"
                },
                "probabilities": probabilities
            }
            
            elapsed_time = time.time() - start_time
            logger.info(f"Prediction completed in {elapsed_time:.2f} seconds")
            return result
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return {"error": f"Error in prediction: {e}"} 