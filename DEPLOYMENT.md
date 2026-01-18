# FlyFair Deployment Guide

## Deployment Status

- **Backend**: Railway (Free Tier)
- **Frontend**: Vercel (Free Tier)
- **Mode**: RAG-only (no LLM in production)

## Backend Deployment (Railway)

### Prerequisites
- Railway account (free tier)
- GitHub repository connected

### Steps

1. **Create Railway Project**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select the FlyFair repository
   - Choose the `backend/` directory

2. **Configuration**
   - Railway will auto-detect Python
   - Uses `Procfile` or `railway.json` for start command
   - Port is set via `$PORT` environment variable (Railway sets this automatically)

3. **No Environment Variables Required**
   - LLM is disabled in production (`use_llm=False`)
   - RAG-only mode works without any API keys

4. **Verify Deployment**
   - Check `/health` endpoint: `https://your-app.railway.app/health`
   - Check `/` endpoint: `https://your-app.railway.app/`

### Expected Build Time
- Initial build: 5-8 minutes (downloads sentence-transformers model)
- Subsequent builds: 3-5 minutes

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier)
- GitHub repository connected

### Steps

1. **Create Vercel Project**
   - Go to https://vercel.com
   - Click "Add New Project"
   - Import GitHub repository
   - Set Root Directory to `frontend/`

2. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` = `https://your-backend.railway.app`
   - This connects frontend to the Railway backend

3. **Build Settings**
   - Framework Preset: Next.js (auto-detected)
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `.next` (auto-detected)

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy automatically

### Post-Deployment

1. **Update Backend CORS** (if needed)
   - If CORS issues occur, update `backend/main.py`:
   ```python
   allow_origins=["https://your-frontend.vercel.app"]
   ```
   - Currently set to `["*"]` which should work for all origins

2. **Test Integration**
   - Visit Vercel URL
   - Try a query: "My flight is delayed by 3 hours"
   - Verify response format is correct

## Production Configuration

### Backend (`backend/main.py`)
- `use_llm=False` by default
- CORS enabled for all origins
- Lazy RAG loading (loads on first query)

### Frontend (`frontend/components/ChatInterface.tsx`)
- `use_llm=false` hardcoded
- API URL from `NEXT_PUBLIC_API_URL` env var

## Troubleshooting

### Backend Issues

**Build fails with "Out of memory"**
- Railway free tier has limits
- Solution: Use smaller model or upgrade

**RAG service takes long to load**
- First request is slow (building FAISS index)
- Solution: Acceptable for free tier, or implement warm-up endpoint

**CORS errors**
- Check `allow_origins` in `main.py`
- Ensure frontend URL is correct

### Frontend Issues

**API calls fail**
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Ensure backend is accessible publicly
- Check browser console for errors

**Build fails**
- Ensure all dependencies are in `package.json`
- Check Node.js version compatibility

## Monitoring

### Railway
- View logs: Railway dashboard → Deployments → View Logs
- Metrics: Available in Railway dashboard

### Vercel
- View logs: Vercel dashboard → Deployments → View Function Logs
- Analytics: Available in Vercel dashboard

## Cost

- **Railway**: Free tier (500 hours/month)
- **Vercel**: Free tier (unlimited)
- **Total**: $0/month

## Security Notes

- No API keys required
- No authentication needed
- CORS configured for public access
- All data from public DGCA charter (no sensitive data)
