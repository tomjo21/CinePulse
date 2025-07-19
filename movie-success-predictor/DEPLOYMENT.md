# 🚀 Deployment Guide

This guide covers deploying your Movie Success Predictor application to various hosting platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ All model files in the backend directory (`saved_model.pkl`, `*.joblib`)
- ✅ Updated README.md with your information
- ✅ Working local version
- ✅ Git repository set up

## 🎯 Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend) - Recommended

#### Frontend Deployment (Vercel)

1. **Build the Frontend**
   ```bash
   cd movie-success-predictor
   npm run build
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Connect your GitHub repository
   - Set build settings:
     - **Framework Preset**: Vite
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
     - **Install Command**: `npm install`

3. **Environment Variables** (if needed)
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

#### Backend Deployment (Render)

1. **Prepare Backend**
   - Ensure all model files are in the backend directory
   - Verify `requirements.txt` is up to date

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Create a new **Web Service**
   - Connect your GitHub repository
   - Set configuration:
     - **Name**: `movie-predictor-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd backend && python app.py`
     - **Root Directory**: `backend`

3. **Environment Variables**
   ```
   FLASK_ENV=production
   PORT=10000
   ```

4. **Update Frontend API URL**
   - In your Vite config, update the proxy target to your Render URL
   - Or use environment variables for the API URL

### Option 2: Railway (Full Stack)

1. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway will auto-detect the project structure

2. **Configure Services**
   - **Frontend Service**:
     - Build Command: `npm install && npm run build`
     - Start Command: `npm run preview`
   - **Backend Service**:
     - Build Command: `cd backend && pip install -r requirements.txt`
     - Start Command: `cd backend && python app.py`

### Option 3: Netlify (Frontend) + Railway (Backend)

#### Frontend (Netlify)
1. **Build Settings**
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Node version: `18`

2. **Redirects** (for SPA routing)
   Create `public/_redirects`:
   ```
   /*    /index.html   200
   ```

#### Backend (Railway)
- Same as Option 2 backend setup

### Option 4: Docker Deployment

1. **Build Docker Image**
   ```bash
   docker build -t movie-predictor .
   ```

2. **Run Container**
   ```bash
   docker run -p 5000:5000 movie-predictor
   ```

3. **Deploy to Docker Platforms**
   - **Railway**: Supports Docker deployments
   - **Render**: Supports Docker deployments
   - **DigitalOcean App Platform**: Native Docker support

## 🔧 Configuration Files

### Vite Config Updates
```typescript
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/predict': {
        target: process.env.VITE_API_URL || 'http://localhost:5000',
        changeOrigin: true,
      },
      '/health': {
        target: process.env.VITE_API_URL || 'http://localhost:5000',
        changeOrigin: true,
      },
      '/final_tmdb_cleaned.csv': {
        target: process.env.VITE_API_URL || 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
});
```

### Backend Environment Variables
```env
FLASK_ENV=production
PORT=10000
HOST=0.0.0.0
```

## 📁 File Structure for Deployment

Ensure your repository has this structure:
```
movie-success-predictor/
├── src/                    # React source
├── backend/
│   ├── app.py             # Flask app
│   ├── saved_model.pkl    # ML model
│   ├── *.joblib           # Success rate files
│   └── requirements.txt   # Python deps
├── public/
│   └── final_tmdb_cleaned.csv
├── package.json
├── vite.config.ts
├── .gitignore
└── README.md
```

## 🚨 Common Issues & Solutions

### 1. Model Files Not Found
**Issue**: Backend can't find model files
**Solution**: Ensure all `.pkl` and `.joblib` files are in the backend directory

### 2. CORS Errors
**Issue**: Frontend can't connect to backend
**Solution**: Verify CORS settings in `app.py` and proxy configuration

### 3. Build Failures
**Issue**: Frontend build fails
**Solution**: Check Node.js version and dependencies

### 4. Port Issues
**Issue**: Backend won't start
**Solution**: Use environment variable for PORT (e.g., `PORT=10000`)

### 5. CSV File Not Loading
**Issue**: Movie search doesn't work
**Solution**: Ensure CSV route is added to backend and proxy is configured

## 🔍 Testing Deployment

### Health Check
```bash
curl https://your-backend-url.com/health
```

### API Test
```bash
curl -X POST https://your-backend-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "movie_title": "Test Movie",
    "director": "Test Director",
    "actor1": "Actor 1",
    "actor2": "Actor 2", 
    "actor3": "Actor 3",
    "budget": 50000000,
    "runtime": 120,
    "genres": "Action",
    "production_companies": "Test Studio",
    "original_language": "en",
    "release_year": 2024,
    "release_month": 6,
    "avg_rating": 7.5,
    "ratings_count": 1000
  }'
```

## 📊 Monitoring

### Backend Monitoring
- Check Render/Railway logs for errors
- Monitor API response times
- Set up health check alerts

### Frontend Monitoring
- Use Vercel/Netlify analytics
- Monitor Core Web Vitals
- Check for JavaScript errors

## 🔄 Continuous Deployment

### GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🎉 Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] Movie search functionality works
- [ ] New movie prediction works
- [ ] All API endpoints respond correctly
- [ ] CORS issues resolved
- [ ] Environment variables set correctly
- [ ] Domain/URL configured
- [ ] SSL certificate active
- [ ] Performance monitoring set up

## 📞 Support

If you encounter issues:
1. Check the platform's documentation
2. Review logs for error messages
3. Test locally first
4. Verify all files are committed to Git
5. Check environment variables

---

**Happy Deploying! 🚀** 