# Phase 2 Quick Start Guide

## Current Status
✅ All code implemented (backend + frontend)
✅ Setup script created
⏸️ Waiting for database credentials

## Step-by-Step Setup

### Step 1: Add Your Neon Database Credentials

Open `c:\development-file\Hackaton-2\Phase-2\details.md` and replace the placeholder values:

**Before:**
```
DATABASE_URL=postgresql://[username]:[password]@[host]/[database]?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-here-change-this-to-something-secure
```

**After (example with your actual credentials):**
```
DATABASE_URL=postgresql://myuser:mypass123@ep-cool-sound-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=my-super-secure-secret-key-that-is-at-least-32-characters-long
```

**Where to get these:**
- **DATABASE_URL**: From your Neon dashboard → Connection Details → Connection String
- **BETTER_AUTH_SECRET**: Generate a random 32+ character string (or use the PowerShell command below)

**Generate a secure secret (Windows PowerShell):**
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

---

### Step 2: Run the Setup Script

Once you've added your credentials to `details.md`, run:

```bash
cd c:\development-file\Hackaton-2\Phase-2
python setup-env.py
```

This will:
- ✅ Validate your credentials
- ✅ Create `project/backend/.env`
- ✅ Create `project/frontend/.env.local`
- ✅ Show you the next steps

---

### Step 3: Install Backend Dependencies

```bash
cd c:\development-file\Hackaton-2\Phase-2\project\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 4: Run Backend Tests (Verify Everything Works)

```bash
# Make sure you're in backend directory with venv activated
pytest -v
```

**Expected result:** All 65 tests should pass ✅

---

### Step 5: Start the Backend Server

```bash
# In backend directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Test the health endpoint:**
Open browser to: http://localhost:8000/health
Should see: `{"status":"healthy"}`

---

### Step 6: Install Frontend Dependencies

Open a **new terminal**:

```bash
cd c:\development-file\Hackaton-2\Phase-2\project\frontend
npm install
```

---

### Step 7: Start the Frontend Server

```bash
# In frontend directory
npm run dev
```

**Expected output:**
```
▲ Next.js 16.x.x
- Local:        http://localhost:3000
```

---

### Step 8: Test the Application

1. **Open browser:** http://localhost:3000

2. **Test Sign Up:**
   - Click "Sign Up"
   - Enter email, password, and name
   - Should redirect to tasks page

3. **Test Task Management:**
   - Create a new task
   - Mark it as complete
   - Edit the task
   - Delete the task

4. **Test User Isolation:**
   - Sign out
   - Create a second user account
   - Verify each user only sees their own tasks

---

## Troubleshooting

### "Connection refused" error
- ✅ Check DATABASE_URL is correct
- ✅ Verify Neon project is active (not paused)
- ✅ Ensure `?sslmode=require` is at the end of the URL

### "Authentication failed" error
- ✅ Verify BETTER_AUTH_SECRET matches in both .env files
- ✅ Check secret is at least 32 characters
- ✅ Clear browser localStorage and try again

### "CORS error" in browser
- ✅ Verify backend CORS_ORIGINS includes http://localhost:3000
- ✅ Restart backend server after changing .env
- ✅ Check frontend is running on port 3000

### Tests failing
- ✅ Ensure database connection is working
- ✅ Check all dependencies are installed
- ✅ Verify Python version is 3.11+

---

## What You Should See

**Backend (Terminal 1):**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Frontend (Terminal 2):**
```
▲ Next.js 16.x.x
✓ Ready in 2.5s
- Local:        http://localhost:3000
```

**Browser (http://localhost:3000):**
- Landing page with "Sign Up" and "Sign In" buttons
- After signup: Tasks dashboard with "Add Task" button
- Responsive design with Tailwind CSS styling

---

## Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the detailed setup guide: `DATABASE-SETUP.md`
3. Check backend logs for error messages
4. Verify all environment variables are set correctly

---

## Next Steps After Setup

Once everything is working:
1. ✅ Complete Phase 2 testing
2. 📝 Document any issues or improvements
3. 🚀 Prepare for Phase 3 (AI Chatbot)
4. 📊 Review test coverage and code quality

---

**Ready to start? Add your credentials to `details.md` and run `python setup-env.py`**
