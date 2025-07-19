// Test script to verify frontend-backend integration
const fetch = require('node-fetch');

async function testFrontendIntegration() {
    console.log('🧪 Testing Frontend-Backend Integration...');
    console.log('=' * 50);
    
    const baseUrl = 'http://localhost:5000';
    
    // Test 1: Health check
    console.log('\n1. Testing Health Check...');
    try {
        const response = await fetch(`${baseUrl}/health`);
        const data = await response.json();
        console.log('✅ Health check passed:', data);
    } catch (error) {
        console.log('❌ Health check failed:', error.message);
        return false;
    }
    
    // Test 2: Model info
    console.log('\n2. Testing Model Info...');
    try {
        const response = await fetch(`${baseUrl}/model-info`);
        const data = await response.json();
        console.log('✅ Model info:', data);
    } catch (error) {
        console.log('❌ Model info failed:', error.message);
        return false;
    }
    
    // Test 3: CSV file access (for movie search)
    console.log('\n3. Testing CSV File Access...');
    try {
        const response = await fetch(`${baseUrl}/final_tmdb_cleaned.csv`);
        if (response.ok) {
            console.log('✅ CSV file accessible');
        } else {
            console.log('❌ CSV file not accessible:', response.status);
        }
    } catch (error) {
        console.log('❌ CSV file access failed:', error.message);
    }
    
    // Test 4: Prediction API (simulating frontend form submission)
    console.log('\n4. Testing Prediction API...');
    const testMovie = {
        movie_title: "Test Movie",
        director: "Christopher Nolan",
        actor1: "Leonardo DiCaprio",
        actor2: "Tom Hanks",
        actor3: "Morgan Freeman",
        budget: 150000000,
        runtime: 138,
        genres: "Action",
        production_companies: "Warner Bros.",
        original_language: "en",
        release_year: 2024,
        release_month: 6,
        avg_rating: 8.2,
        ratings_count: 50000
    };
    
    try {
        const response = await fetch(`${baseUrl}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testMovie),
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Prediction successful:', {
                movie: data.movie_title,
                prediction: data.prediction,
                confidence: data.confidence,
                factors: data.features_used
            });
        } else {
            console.log('❌ Prediction failed:', response.status, await response.text());
            return false;
        }
    } catch (error) {
        console.log('❌ Prediction error:', error.message);
        return false;
    }
    
    // Test 5: CORS headers
    console.log('\n5. Testing CORS Headers...');
    try {
        const response = await fetch(`${baseUrl}/predict`, {
            method: 'OPTIONS',
        });
        
        const corsHeaders = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        };
        
        console.log('✅ CORS headers:', corsHeaders);
    } catch (error) {
        console.log('❌ CORS test failed:', error.message);
    }
    
    console.log('\n' + '=' * 50);
    console.log('🎉 Frontend-Backend Integration Test Complete!');
    return true;
}

// Run the test
testFrontendIntegration().then(success => {
    if (!success) {
        console.log('\n❌ Some tests failed. Check the backend logs.');
        process.exit(1);
    }
}).catch(error => {
    console.log('\n❌ Test failed with error:', error);
    process.exit(1);
}); 