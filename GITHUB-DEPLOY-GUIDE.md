# GitHub Repository Setup Guide

## Step 1: Create GitHub Repositories

Go to https://github.com/new and create these repositories:

1. **Phase-2-Todo-App** (or your preferred name)
   - Description: "Phase 2 - Full-stack Todo Application with Next.js and FastAPI"
   - Public or Private: Your choice
   - DO NOT initialize with README (we already have code)

2. **Phase-3-AI-Chatbot** (for later)
3. **Phase-4-Docker-K8s** (for later)
4. **Phase-5-Kafka-Dapr** (for later)

## Step 2: Get Repository URL

After creating the repository, copy the HTTPS URL:
```
https://github.com/YOUR_USERNAME/Phase-2-Todo-App.git
```

## Step 3: Push Code to GitHub

I'll run these commands once you provide the URL:
```bash
cd "C:\development-file\Hackaton-2\Phase-2 - clone"
git remote add origin https://github.com/YOUR_USERNAME/Phase-2-Todo-App.git
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Vercel

### Option A: Via Vercel Dashboard (Recommended)
1. Go to https://vercel.com/new
2. Sign in with GitHub
3. Import your repository: Phase-2-Todo-App
4. Configure:
   - Framework Preset: Next.js
   - Root Directory: `project/frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Environment Variables:
     - `NEXT_PUBLIC_USE_MOCK_DATA` = `true`
5. Click "Deploy"
6. Copy the deployment URL

### Option B: Via CLI (Alternative)
```bash
cd project/frontend
npx vercel --prod
```

## Step 5: Test Deployment

Once deployed, test these URLs:
- Landing page: https://your-app.vercel.app
- Sign in: https://your-app.vercel.app/signin
- Sign up: https://your-app.vercel.app/signup

Demo credentials (mock data):
- Email: demo@example.com
- Password: demo123

---

## Quick Action Required

**Please provide your GitHub username or the repository URL you just created, and I'll push the code immediately.**

Example: `https://github.com/yourusername/Phase-2-Todo-App.git`
