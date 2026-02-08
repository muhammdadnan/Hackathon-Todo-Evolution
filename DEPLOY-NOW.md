# Vercel Deployment - Step by Step

## Quick Deploy (5 minutes)

### Step 1: Start Deployment
Open a new terminal and run:
```bash
cd "C:\development-file\Hackaton-2\Phase-2 - clone\project\frontend"
npx vercel --prod
```

### Step 2: Authenticate
- Browser will open automatically
- Sign in with GitHub, GitLab, or Email
- Authorize Vercel CLI

### Step 3: Answer Prompts
```
? Set up and deploy "~/project/frontend"? [Y/n] Y
? Which scope? [Use arrows] → Select your account
? Link to existing project? [y/N] N
? What's your project's name? phase-2-todo-app
? In which directory is your code located? ./ [Press Enter]
? Want to override the settings? [y/N] N
```

### Step 4: Wait for Deployment
- Build will start automatically
- Takes ~2-3 minutes
- You'll get a URL like: `https://phase-2-todo-app-xxx.vercel.app`

### Step 5: Test Your App
Visit the URL and test:
- Landing page: `https://your-url.vercel.app`
- Sign in with: `demo@example.com` / `demo123`
- Create, edit, complete, delete tasks

---

## Alternative: Vercel Dashboard (If CLI Fails)

1. Go to: https://vercel.com/new
2. Click "Continue with GitHub" (or other method)
3. Skip GitHub import, click "Deploy from template" or "Import project"
4. Upload the `project/frontend` folder as ZIP
5. Set environment variable: `NEXT_PUBLIC_USE_MOCK_DATA=true`
6. Click "Deploy"

---

## What to Copy for Submission
After deployment, copy:
- ✅ Deployment URL: `https://phase-2-todo-app-xxx.vercel.app`
- ✅ GitHub URL: (we'll do this after if needed)

---

**Ready? Run the command above in your terminal!**
