from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["*"], methods=["GET", "POST", "OPTIONS"])  # Enable CORS for all routes

# Global variables to store loaded model and data
pipeline = None
director_success_rates = None
actor1_success_rates = None
actor2_success_rates = None
actor3_success_rates = None

def load_model_and_data():
    """Load the saved model and success rate dictionaries using joblib"""
    global pipeline, director_success_rates, actor1_success_rates, actor2_success_rates, actor3_success_rates
    
    try:
        # Load the main model
        model_path = os.path.join(os.path.dirname(__file__), 'saved_model.pkl')
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at: {model_path}")
            return False
            
        pipeline = joblib.load(model_path)
        logger.info("Main model loaded successfully")
        
        # Load success rate dictionaries
        director_path = os.path.join(os.path.dirname(__file__), 'director_success.joblib')
        actor1_path = os.path.join(os.path.dirname(__file__), 'actor1_success.joblib')
        actor2_path = os.path.join(os.path.dirname(__file__), 'actor2_success.joblib')
        actor3_path = os.path.join(os.path.dirname(__file__), 'actor3_success.joblib')
        
        # Load director success rates
        if os.path.exists(director_path):
            director_success_rates = joblib.load(director_path)
            logger.info(f"Director success rates loaded: {len(director_success_rates)} entries")
        else:
            logger.warning(f"Director success rates file not found at: {director_path}")
            director_success_rates = {}
        
        # Load actor success rates
        if os.path.exists(actor1_path):
            actor1_success_rates = joblib.load(actor1_path)
            logger.info(f"Actor1 success rates loaded: {len(actor1_success_rates)} entries")
        else:
            logger.warning(f"Actor1 success rates file not found at: {actor1_path}")
            actor1_success_rates = {}
            
        if os.path.exists(actor2_path):
            actor2_success_rates = joblib.load(actor2_path)
            logger.info(f"Actor2 success rates loaded: {len(actor2_success_rates)} entries")
        else:
            logger.warning(f"Actor2 success rates file not found at: {actor2_path}")
            actor2_success_rates = {}
            
        if os.path.exists(actor3_path):
            actor3_success_rates = joblib.load(actor3_path)
            logger.info(f"Actor3 success rates loaded: {len(actor3_success_rates)} entries")
        else:
            logger.warning(f"Actor3 success rates file not found at: {actor3_path}")
            actor3_success_rates = {}
        
        logger.info("All model and success rate data loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model and data: {str(e)}")
        return False

def get_success_rate(name, success_rates_dict, default_rate=0.5):
    """Get success rate for a person, handling missing keys gracefully"""
    if not name or not name.strip():
        return default_rate
    
    # Try exact match first
    if name in success_rates_dict:
        return success_rates_dict[name]
    
    # Try case-insensitive match
    name_lower = name.lower().strip()
    for key, value in success_rates_dict.items():
        if key.lower().strip() == name_lower:
            return value
    
    # Return default if not found
    return default_rate

def prepare_features(movie_data):
    """Prepare features for prediction using the loaded success rates"""
    try:
        # Get director success rate
        director = movie_data.get('director', '')
        director_success_rate = get_success_rate(director, director_success_rates)
        
        # Get actor success rates
        actor1 = movie_data.get('actor1', '')
        actor2 = movie_data.get('actor2', '')
        actor3 = movie_data.get('actor3', '')
        
        actor1_success_rate = get_success_rate(actor1, actor1_success_rates)
        actor2_success_rate = get_success_rate(actor2, actor2_success_rates)
        actor3_success_rate = get_success_rate(actor3, actor3_success_rates)
        
        # Create features DataFrame that matches the training data format
        features = {
            'budget': float(movie_data.get('budget', 0)),
            'runtime': float(movie_data.get('runtime', 0)),
            'release_year': int(movie_data.get('release_year', 2024)),
            'release_month': int(movie_data.get('release_month', 6)),
            'avg_rating': float(movie_data.get('avg_rating', 7.0)),
            'ratings_count': int(movie_data.get('ratings_count', 1000)),
            'director_success_rate': director_success_rate,
            'actor1_success_rate': actor1_success_rate,
            'actor2_success_rate': actor2_success_rate,
            'actor3_success_rate': actor3_success_rate,
            'genres': str(movie_data.get('genres', 'Drama')),
            'original_language': str(movie_data.get('original_language', 'en')),
            'production_companies': str(movie_data.get('production_companies', 'Independent'))
        }
        
        return features
        
    except Exception as e:
        logger.error(f"Error preparing features: {str(e)}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': pipeline is not None,
        'director_success_rates_loaded': director_success_rates is not None,
        'actor_success_rates_loaded': all([actor1_success_rates, actor2_success_rates, actor3_success_rates]),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """Predict movie success endpoint"""
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        # Check if model is loaded
        if pipeline is None:
            return jsonify({
                'error': 'Model not loaded. Please ensure saved_model.pkl is available.'
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = [
            'movie_title', 'director', 'actor1', 'actor2', 'actor3', 
            'budget', 'runtime', 'genres', 'production_companies', 
            'original_language', 'release_year', 'release_month', 
            'avg_rating', 'ratings_count'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Prepare features
        features = prepare_features(data)
        
        # Convert to DataFrame for prediction
        feature_df = pd.DataFrame([features])
        
        # Make prediction
        prediction = pipeline.predict(feature_df)[0]
        probability = pipeline.predict_proba(feature_df)[0]
        
        # Convert prediction to HIT/FLOP
        result = "HIT" if prediction == 1 else "FLOP"
        
        # Get probability for the predicted class
        hit_probability = probability[1] if prediction == 1 else probability[0]
        
        # Create meaningful factors list
        factors = []
        if features['director_success_rate'] > 0.7:
            factors.append(f"Strong director track record ({features['director_success_rate']:.1%})")
        if features['actor1_success_rate'] > 0.7:
            factors.append(f"Lead actor success rate ({features['actor1_success_rate']:.1%})")
        if features['budget'] > 100000000:
            factors.append("High production budget")
        elif features['budget'] < 20000000:
            factors.append("Low budget risk")
        if features['avg_rating'] > 7.5:
            factors.append(f"High audience rating ({features['avg_rating']:.1f}/10)")
        if features['genres'] in ['Action', 'Adventure', 'Comedy']:
            factors.append("Popular genre")
        
        if not factors:
            factors = ["Standard market conditions"]
        
        logger.info(f"Prediction for '{data['movie_title']}': {result} (probability: {hit_probability:.3f})")
        
        response_data = {
            'movie_title': data['movie_title'],
            'prediction': result,
            'probability': round(hit_probability, 3),
            'confidence': round(hit_probability * 100, 1),
            'features_used': factors,
            'timestamp': datetime.now().isoformat()
        }
        
        response = jsonify(response_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        error_response = jsonify({
            'error': f'Prediction failed: {str(e)}'
        })
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    if pipeline is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    response_data = {
        'model_type': type(pipeline).__name__,
        'director_count': len(director_success_rates) if director_success_rates else 0,
        'actor1_count': len(actor1_success_rates) if actor1_success_rates else 0,
        'actor2_count': len(actor2_success_rates) if actor2_success_rates else 0,
        'actor3_count': len(actor3_success_rates) if actor3_success_rates else 0,
        'model_loaded_at': datetime.now().isoformat()
    }
    
    response = jsonify(response_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/final_tmdb_cleaned.csv')
def serve_csv():
    """Serve the movie data CSV file"""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'public', 'final_tmdb_cleaned.csv')
    if os.path.exists(csv_path):
        return send_from_directory(os.path.dirname(csv_path), 'final_tmdb_cleaned.csv')
    else:
        return jsonify({'error': 'CSV file not found'}), 404

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    build_dir = os.path.join(os.path.dirname(__file__), 'build')
    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    else:
        return send_from_directory(build_dir, 'index.html')

if __name__ == '__main__':
    # Load model on startup
    if load_model_and_data():
        logger.info("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to load model. Server not started.")
        exit(1) 