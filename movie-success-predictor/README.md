# 🎬 Movie Success Predictor

A full-stack web application that predicts whether a movie will be a HIT or FLOP using machine learning. Built with React, Flask, and scikit-learn.

## ✨ Features

- **Movie Success Prediction**: Predict if a movie will be successful based on various factors
- **Existing Movie Search**: Search through a database of 3000+ movies with their predictions
- **New Movie Analysis**: Enter details for a new movie to get predictions
- **Interactive UI**: Modern, responsive interface with real-time predictions
- **Machine Learning Model**: Random Forest model trained on TMDB dataset

## 🚀 Live Demo

[Add your deployed URL here]

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Shadcn/ui** components
- **Lucide React** icons

### Backend
- **Flask** Python web framework
- **scikit-learn** for machine learning
- **pandas** for data processing
- **joblib** for model serialization

### Data
- **TMDB Dataset** with 3000+ movies
- **Random Forest** model for predictions
- **Success rate analysis** for directors and actors

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

### Clone the Repository
```bash
git clone https://github.com/yourusername/movie-success-predictor.git
cd movie-success-predictor
```

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The application will be available at:
- Frontend: http://localhost:8080
- Backend API: http://localhost:5000

## 🎯 Usage

### Search Existing Movies
1. Go to the "Search Existing Movies" section
2. Type a movie title, director, or genre
3. Click on any movie to see its prediction details

### Predict New Movie
1. Navigate to the "Predict New Movie" section
2. Fill in all required fields:
   - Movie title
   - Director
   - Lead actors (3)
   - Budget
   - Runtime
   - Genre
   - Production companies
   - Release year/month
   - Expected rating
3. Click "Predict Success" to get results

## 📊 Model Information

The prediction model uses the following features:
- **Budget**: Production budget in USD
- **Runtime**: Movie duration in minutes
- **Release timing**: Year and month
- **Ratings**: Expected audience rating and count
- **Cast success rates**: Historical success of director and actors
- **Genre**: Movie genre classification
- **Production**: Studio and language information

## 🚀 Deployment

### Frontend Deployment (Vercel/Netlify)
```bash
# Build the frontend
npm run build

# Deploy the dist folder to your preferred platform
```

### Backend Deployment (Render/Railway)
1. Ensure all model files are in the backend directory
2. Set environment variables if needed
3. Deploy using the platform's Python template

### Environment Variables
```env
FLASK_ENV=production
PORT=5000
```

## 📁 Project Structure

```
movie-success-predictor/
├── src/                    # React frontend source
│   ├── components/         # React components
│   ├── data/              # Data services
│   ├── pages/             # Page components
│   └── ui/                # UI components
├── backend/               # Flask backend
│   ├── app.py            # Main Flask application
│   ├── saved_model.pkl   # Trained ML model
│   ├── *.joblib          # Success rate data
│   └── requirements.txt  # Python dependencies
├── public/               # Static assets
│   └── final_tmdb_cleaned.csv  # Movie dataset
└── package.json          # Node.js dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TMDB** for the movie dataset
- **scikit-learn** for the machine learning framework
- **React** and **Flask** communities for excellent documentation

## 📞 Contact

Your Name - [your.email@example.com](mailto:your.email@example.com)

Project Link: [https://github.com/yourusername/movie-success-predictor](https://github.com/yourusername/movie-success-predictor)
