import requests
import json
import time

def test_backend():
    """Test the backend API endpoints"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Movie Success Predictor Backend...")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Model Info
    print("\n2. Testing Model Info...")
    try:
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model info: {data}")
        else:
            print(f"❌ Model info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model info error: {e}")
        return False
    
    # Test 3: Prediction with known director/actor
    print("\n3. Testing Prediction with known director/actor...")
    test_movie = {
        "movie_title": "The Matrix Reloaded",
        "director": "Christopher Nolan",
        "actor1": "Leonardo DiCaprio",
        "actor2": "Tom Hanks",
        "actor3": "Morgan Freeman",
        "budget": 150000000,
        "runtime": 138,
        "genres": "Action",
        "production_companies": "Warner Bros.",
        "original_language": "en",
        "release_year": 2024,
        "release_month": 6,
        "avg_rating": 8.2,
        "ratings_count": 50000
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=test_movie,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Movie: {data['movie_title']}")
            print(f"   Prediction: {data['prediction']}")
            print(f"   Confidence: {data['confidence']}%")
            print(f"   Factors: {data['features_used']}")
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False
    
    # Test 4: Prediction with unknown director/actor (test graceful handling)
    print("\n4. Testing Prediction with unknown director/actor...")
    test_movie_unknown = {
        "movie_title": "Unknown Movie",
        "director": "Unknown Director",
        "actor1": "Unknown Actor",
        "actor2": "Another Unknown",
        "actor3": "Yet Another Unknown",
        "budget": 50000000,
        "runtime": 120,
        "genres": "Drama",
        "production_companies": "Independent",
        "original_language": "en",
        "release_year": 2024,
        "release_month": 6,
        "avg_rating": 6.5,
        "ratings_count": 1000
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=test_movie_unknown,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Unknown actor/director prediction successful!")
            print(f"   Movie: {data['movie_title']}")
            print(f"   Prediction: {data['prediction']}")
            print(f"   Confidence: {data['confidence']}%")
        else:
            print(f"❌ Unknown actor/director prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Unknown actor/director prediction error: {e}")
        return False
    
    # Test 5: CORS preflight request
    print("\n5. Testing CORS preflight request...")
    try:
        response = requests.options(f"{base_url}/predict")
        if response.status_code == 200:
            print(f"✅ CORS preflight successful")
            print(f"   CORS headers: {dict(response.headers)}")
        else:
            print(f"❌ CORS preflight failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS preflight error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Backend is working correctly.")
    return True

if __name__ == "__main__":
    # Wait a bit for the server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    success = test_backend()
    if not success:
        print("\n❌ Some tests failed. Check the server logs.")
        exit(1) 