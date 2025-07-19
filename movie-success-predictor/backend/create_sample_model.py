import numpy as np
import pandas as pd
import joblib
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

warnings.filterwarnings('ignore')

def create_sample_model():
    """Create a sample model using the same approach as the Colab code"""
    
    print("🎬 Creating sample movie success prediction model...")
    
    # Create synthetic data similar to TMDB dataset
    np.random.seed(42)
    n_samples = 3000
    
    # Generate realistic movie data
    budget = np.random.uniform(100000, 300000000, n_samples)
    runtime = np.random.uniform(60, 200, n_samples)
    release_year = np.random.randint(1990, 2025, n_samples)
    release_month = np.random.randint(1, 13, n_samples)
    avg_rating = np.random.uniform(3.0, 9.5, n_samples)
    ratings_count = np.random.uniform(10, 2000000, n_samples)
    
    # Generate director and actor data
    directors = ['Christopher Nolan', 'Steven Spielberg', 'James Cameron', 'Peter Jackson', 
                'Quentin Tarantino', 'Martin Scorsese', 'Ridley Scott', 'Tim Burton', 
                'Guy Ritchie', 'Zack Snyder', 'Unknown Director']
    
    actors = ['Leonardo DiCaprio', 'Tom Hanks', 'Morgan Freeman', 'Brad Pitt', 
             'Johnny Depp', 'Robert Downey Jr.', 'Chris Hemsworth', 'Scarlett Johansson', 
             'Emma Stone', 'Ryan Reynolds', 'Unknown Actor']
    
    genres_list = ['Action', 'Adventure', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 
                   'Thriller', 'Romance', 'Animation', 'Documentary', 'Fantasy', 'Mystery']
    
    languages = ['en', 'es', 'fr', 'de', 'it', 'ja', 'ko', 'zh']
    
    companies_list = ['Warner Bros.', 'Universal Pictures', 'Paramount Pictures', 
                     '20th Century Fox', 'Sony Pictures', 'Walt Disney Pictures',
                     'Columbia Pictures', 'New Line Cinema', 'DreamWorks', 'Independent']
    
    # Generate random data
    director = np.random.choice(directors, n_samples)
    actor1 = np.random.choice(actors, n_samples)
    actor2 = np.random.choice(actors, n_samples)
    actor3 = np.random.choice(actors, n_samples)
    genres = np.random.choice(genres_list, n_samples)
    original_language = np.random.choice(languages, n_samples)
    production_companies = np.random.choice(companies_list, n_samples)
    
    # Create success rate mappings (matching Colab code format)
    director_success_rates = {
        'Christopher Nolan': 0.85,
        'Steven Spielberg': 0.80,
        'James Cameron': 0.75,
        'Peter Jackson': 0.70,
        'Quentin Tarantino': 0.65,
        'Martin Scorsese': 0.75,
        'Ridley Scott': 0.60,
        'Tim Burton': 0.55,
        'Guy Ritchie': 0.50,
        'Zack Snyder': 0.45,
        'Unknown Director': 0.50
    }
    
    actor_success_rates = {
        'Leonardo DiCaprio': 0.80,
        'Tom Hanks': 0.85,
        'Morgan Freeman': 0.75,
        'Brad Pitt': 0.70,
        'Johnny Depp': 0.65,
        'Robert Downey Jr.': 0.75,
        'Chris Hemsworth': 0.70,
        'Scarlett Johansson': 0.65,
        'Emma Stone': 0.60,
        'Ryan Reynolds': 0.55,
        'Unknown Actor': 0.50
    }
    
    # Calculate success rates for each movie
    director_success_rate = [director_success_rates.get(d, 0.5) for d in director]
    actor1_success_rate = [actor_success_rates.get(a, 0.5) for a in actor1]
    actor2_success_rate = [actor_success_rates.get(a, 0.5) for a in actor2]
    actor3_success_rate = [actor_success_rates.get(a, 0.5) for a in actor3]
    
    # Create DataFrame
    movies = pd.DataFrame({
        'budget': budget,
        'runtime': runtime,
        'release_year': release_year,
        'release_month': release_month,
        'avg_rating': avg_rating,
        'ratings_count': ratings_count,
        'director': director,
        'actor1': actor1,
        'actor2': actor2,
        'actor3': actor3,
        'genres': genres,
        'original_language': original_language,
        'production_companies': production_companies,
        'director_success_rate': director_success_rate,
        'actor1_success_rate': actor1_success_rate,
        'actor2_success_rate': actor2_success_rate,
        'actor3_success_rate': actor3_success_rate
    })
    
    # Define success criteria (similar to Colab code)
    movies['success'] = ((movies['avg_rating'] > 6.5) & 
                        (movies['budget'] > 20000000) & 
                        (movies['director_success_rate'] > 0.5) & 
                        (movies['actor1_success_rate'] > 0.4)).astype(int)
    
    # Features for modeling (matching the backend expectations)
    features = [
        'budget', 'runtime', 'genres', 'original_language', 'avg_rating',
        'ratings_count', 'release_year', 'release_month',
        'director_success_rate', 'actor1_success_rate',
        'actor2_success_rate', 'actor3_success_rate',
        'production_companies'
    ]
    target = 'success'
    
    X = movies[features]
    y = movies[target]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Preprocessing pipeline (matching Colab code)
    numeric_features = [
        'budget', 'runtime', 'avg_rating', 'ratings_count',
        'release_year', 'release_month', 'director_success_rate',
        'actor1_success_rate', 'actor2_success_rate', 'actor3_success_rate'
    ]
    
    categorical_features = ['genres', 'original_language', 'production_companies']
    
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', max_categories=10))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
    # Random Forest Model
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])
    
    # Train model
    model_pipeline.fit(X_train, y_train)
    y_pred = model_pipeline.predict(X_test)
    y_prob = model_pipeline.predict_proba(X_test)[:, 1]
    
    # Evaluation
    print("\n🔹 Random Forest Results")
    print(f"✅ Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"✅ ROC AUC: {roc_auc_score(y_test, y_prob):.4f}")
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the main model as a simple pipeline (matching Colab format)
    joblib.dump(model_pipeline, 'saved_model.pkl')
    
    # Save success rate dictionaries as separate joblib files (matching Colab format)
    joblib.dump(director_success_rates, 'director_success.joblib')
    joblib.dump(actor_success_rates, 'actor1_success.joblib')
    joblib.dump(actor_success_rates, 'actor2_success.joblib')  # Using same rates for demo
    joblib.dump(actor_success_rates, 'actor3_success.joblib')  # Using same rates for demo
    
    print("\n✅ Model and success rate files saved successfully!")
    print(f"📁 saved_model.pkl - Main model pipeline")
    print(f"📁 director_success.joblib - {len(director_success_rates)} director success rates")
    print(f"📁 actor1_success.joblib - {len(actor_success_rates)} actor1 success rates")
    print(f"📁 actor2_success.joblib - {len(actor_success_rates)} actor2 success rates")
    print(f"📁 actor3_success.joblib - {len(actor_success_rates)} actor3 success rates")
    print(f"🎯 Training samples: {len(X_train)}")
    print(f"🧪 Test samples: {len(X_test)}")

if __name__ == '__main__':
    create_sample_model() 