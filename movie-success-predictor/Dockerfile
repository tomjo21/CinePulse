# Use official Python image as base
FROM python:3.10-slim as base

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js (for building React frontend)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Copy backend requirements and install
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend files
COPY backend/ backend/

# Copy frontend files
COPY src/ src/
COPY package.json package-lock.json vite.config.ts index.html tsconfig.json tsconfig.app.json tsconfig.node.json tailwind.config.ts postcss.config.js ./

# Install frontend dependencies and build
RUN npm install
RUN npm run build

# Move built frontend to backend/build
RUN mkdir -p backend/build && cp -r dist/* backend/build/

# Create the model and success rate files
RUN cd backend && python create_sample_model.py
RUN cd backend && python create_success_rates.py

# Expose port
EXPOSE 5000

# Start Flask app
CMD ["python", "backend/app.py"] 