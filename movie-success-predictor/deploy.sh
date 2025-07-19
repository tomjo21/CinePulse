#!/bin/bash

# Movie Success Predictor Deployment Script
# This script helps deploy the application using Docker

set -e  # Exit on any error

echo "🎬 Movie Success Predictor - Deployment Script"
echo "=============================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    docker-compose down
    echo "✅ Cleanup complete"
}

# Trap to cleanup on exit
trap cleanup EXIT

echo "🔧 Building and starting the application..."

# Build and start the application
docker-compose up --build -d

echo "⏳ Waiting for the application to start..."
sleep 10

# Check if the application is running
echo "🔍 Checking application status..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo ""
    echo "🌐 Access your application at: http://localhost:5000"
    echo "📊 API Health Check: http://localhost:5000/health"
    echo "🤖 Model Info: http://localhost:5000/model-info"
    echo ""
    echo "📝 To stop the application, run: docker-compose down"
    echo "📋 To view logs, run: docker-compose logs -f"
    echo ""
    echo "🎉 Deployment successful!"
else
    echo "❌ Application failed to start properly."
    echo "📋 Checking logs..."
    docker-compose logs
    exit 1
fi

# Keep the script running to maintain the container
echo "🔄 Application is running. Press Ctrl+C to stop."
docker-compose logs -f 