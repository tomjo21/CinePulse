#!/bin/bash

# GitHub Setup Script for Movie Success Predictor
# This script helps you set up your GitHub repository

echo "🎬 Setting up GitHub repository for Movie Success Predictor"
echo "=========================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "backend/app.py" ]; then
    echo "❌ Please run this script from the movie-success-predictor directory"
    exit 1
fi

echo "✅ Git is installed"
echo "✅ In correct directory"

# Initialize git repository (if not already done)
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Initial commit: Movie Success Predictor app

- React frontend with TypeScript and Vite
- Flask backend with scikit-learn model
- Movie prediction functionality
- Search existing movies
- Modern UI with Tailwind CSS"
fi

echo ""
echo "🚀 Next Steps:"
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Name it: movie-success-predictor"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "2. Connect your local repository:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/movie-success-predictor.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Update README.md with your information:"
echo "   - Replace 'yourusername' with your GitHub username"
echo "   - Add your email address"
echo "   - Update the project link"
echo ""
echo "4. Deploy your application:"
echo "   - Follow the DEPLOYMENT.md guide"
echo "   - Recommended: Vercel (frontend) + Render (backend)"
echo ""

echo "🎉 Setup complete! Your project is ready for GitHub and deployment." 