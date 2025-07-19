import os
import joblib
import sys

def test_model_creation():
    """Test if the model can be created and loaded correctly"""
    
    print("🧪 Testing Model Creation...")
    print("=" * 40)
    
    try:
        # Import the model creation function
        from create_sample_model import create_sample_model
        
        # Create the model
        print("📊 Creating sample model...")
        create_sample_model()
        
        # Check if model file exists
        if not os.path.exists('saved_model.pkl'):
            print("❌ Model file was not created")
            return False
        
        print("✅ Model file created successfully")
        
        # Test loading the model
        print("📖 Testing model loading...")
        pipeline = joblib.load('saved_model.pkl')
        
        print("✅ Model loaded successfully")
        
        # Test loading success rate dictionaries
        print("📊 Testing success rate dictionaries...")
        
        success_rate_files = [
            'director_success.joblib',
            'actor1_success.joblib', 
            'actor2_success.joblib',
            'actor3_success.joblib'
        ]
        
        for file_path in success_rate_files:
            if os.path.exists(file_path):
                success_rates = joblib.load(file_path)
                print(f"✅ {file_path} loaded: {len(success_rates)} entries")
            else:
                print(f"❌ {file_path} not found")
                return False
        
        # Test a simple prediction
        print("🎯 Testing prediction...")
        
        # Create test data
        import pandas as pd
        test_data = pd.DataFrame([{
            'budget': 100000000,
            'runtime': 120,
            'release_year': 2024,
            'release_month': 6,
            'avg_rating': 7.5,
            'ratings_count': 10000,
            'director_success_rate': 0.8,
            'actor1_success_rate': 0.7,
            'actor2_success_rate': 0.6,
            'actor3_success_rate': 0.5,
            'genres': 'Action',
            'original_language': 'en',
            'production_companies': 'Warner Bros.'
        }])
        
        # Make prediction
        prediction = pipeline.predict(test_data)[0]
        probability = pipeline.predict_proba(test_data)[0]
        
        print(f"✅ Prediction test successful!")
        print(f"   Prediction: {'HIT' if prediction == 1 else 'FLOP'}")
        print(f"   Probability: {probability}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during model testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_creation()
    if success:
        print("\n🎉 Model creation test passed!")
    else:
        print("\n❌ Model creation test failed!")
        sys.exit(1) 