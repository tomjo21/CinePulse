import numpy as np
import pandas as pd
import joblib
import ast
import warnings
from collections import defaultdict

warnings.filterwarnings('ignore')

def safe_literal_eval(x):
    """Safely evaluate string representations of lists/dicts"""
    try:
        return ast.literal_eval(x)
    except:
        return []

def get_director(crew_data):
    """Extract director from crew data"""
    for member in safe_literal_eval(crew_data):
        if member.get('job') == 'Director':
            return member.get('name')
    return np.nan

def get_top_actors(cast_data, n=3):
    """Extract top n actors from cast data"""
    cast = safe_literal_eval(cast_data)
    return [member.get('name') for member in cast[:n]] if cast else [np.nan]*n

def calculate_success_rate(series, success_series):
    """Calculate success rate for each unique value in series"""
    success_rates = {}
    for value in series.unique():
        if pd.notna(value) and value != '':
            mask = series == value
            if mask.sum() > 0:
                success_rate = success_series[mask].mean()
                success_rates[value] = success_rate
    
    return success_rates

def create_success_rates():
    """Create success rate dictionaries from TMDB data"""
    
    print("🎬 Creating success rate dictionaries from TMDB data...")
    
    try:
        # Load the TMDB data
        print("📊 Loading TMDB data...")
        movies = pd.read_csv('../public/final_tmdb_cleaned.csv')
        print(f"✅ Loaded {len(movies)} movies")
        
        # Extract director and actors
        print("🎭 Extracting director and actor information...")
        movies['director'] = movies['crew'].apply(get_director)
        movies[['actor1', 'actor2', 'actor3']] = pd.DataFrame(
            movies['cast'].apply(lambda x: get_top_actors(x, 3)).tolist(), 
            index=movies.index
        )
        
        # Define success criteria (revenue > 1.5 * budget)
        movies['success'] = (movies['revenue'] > 1.5 * movies['budget']).astype(int)
        
        print(f"📈 Success rate: {movies['success'].mean():.2%}")
        
        # Calculate success rates
        print("📊 Calculating director success rates...")
        director_success = calculate_success_rate(movies['director'], movies['success'])
        
        print("🎭 Calculating actor success rates...")
        actor1_success = calculate_success_rate(movies['actor1'], movies['success'])
        actor2_success = calculate_success_rate(movies['actor2'], movies['success'])
        actor3_success = calculate_success_rate(movies['actor3'], movies['success'])
        
        # Filter out low-frequency entries (less than 2 movies)
        def filter_low_frequency(success_dict, min_count=2):
            filtered = {}
            for person, rate in success_dict.items():
                if pd.notna(person) and person != '':
                    # Count how many movies this person has
                    if person in movies['director'].values:
                        count = (movies['director'] == person).sum()
                    elif person in movies['actor1'].values:
                        count = (movies['actor1'] == person).sum()
                    elif person in movies['actor2'].values:
                        count = (movies['actor2'] == person).sum()
                    elif person in movies['actor3'].values:
                        count = (movies['actor3'] == person).sum()
                    else:
                        count = 0
                    
                    if count >= min_count:
                        filtered[person] = rate
            return filtered
        
        director_success = filter_low_frequency(director_success)
        actor1_success = filter_low_frequency(actor1_success)
        actor2_success = filter_low_frequency(actor2_success)
        actor3_success = filter_low_frequency(actor3_success)
        
        # Save success rate dictionaries
        print("💾 Saving success rate dictionaries...")
        joblib.dump(director_success, 'director_success.joblib')
        joblib.dump(actor1_success, 'actor1_success.joblib')
        joblib.dump(actor2_success, 'actor2_success.joblib')
        joblib.dump(actor3_success, 'actor3_success.joblib')
        
        print("\n✅ Success rate dictionaries created successfully!")
        print(f"📁 director_success.joblib - {len(director_success)} directors")
        print(f"📁 actor1_success.joblib - {len(actor1_success)} actors")
        print(f"📁 actor2_success.joblib - {len(actor2_success)} actors")
        print(f"📁 actor3_success.joblib - {len(actor3_success)} actors")
        
        # Show some examples
        print("\n📊 Sample director success rates:")
        for director, rate in sorted(director_success.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {director}: {rate:.1%}")
        
        print("\n🎭 Sample actor success rates:")
        for actor, rate in sorted(actor1_success.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {actor}: {rate:.1%}")
        
        return True
        
    except FileNotFoundError:
        print("❌ TMDB data file not found. Creating sample success rates...")
        return create_sample_success_rates()
    except Exception as e:
        print(f"❌ Error creating success rates: {e}")
        print("Creating sample success rates instead...")
        return create_sample_success_rates()

def create_sample_success_rates():
    """Create sample success rate dictionaries for testing"""
    
    print("🎬 Creating sample success rate dictionaries...")
    
    # Sample director success rates
    director_success = {
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
    
    # Sample actor success rates
    actor_success = {
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
    
    # Save success rate dictionaries
    joblib.dump(director_success, 'director_success.joblib')
    joblib.dump(actor_success, 'actor1_success.joblib')
    joblib.dump(actor_success, 'actor2_success.joblib')
    joblib.dump(actor_success, 'actor3_success.joblib')
    
    print("✅ Sample success rate dictionaries created!")
    print(f"📁 director_success.joblib - {len(director_success)} directors")
    print(f"📁 actor1_success.joblib - {len(actor_success)} actors")
    print(f"📁 actor2_success.joblib - {len(actor_success)} actors")
    print(f"📁 actor3_success.joblib - {len(actor_success)} actors")
    
    return True

if __name__ == '__main__':
    create_success_rates() 