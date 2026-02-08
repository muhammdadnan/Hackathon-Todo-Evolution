# Database Setup Guide

## Overview
This guide walks you through setting up the Neon PostgreSQL database for the Phase 2 Todo Application.

## Prerequisites
- Neon account (free tier available)
- Backend environment configured

## Step 1: Create Neon Account

1. Go to [https://neon.tech](https://neon.tech)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create Database

1. Log in to Neon console
2. Click "Create Project"
3. Configure project:
   - **Project Name**: `phase-2-todo-app` (or your preferred name)
   - **Region**: Choose closest to your location
   - **PostgreSQL Version**: 15 or later
4. Click "Create Project"

## Step 3: Get Connection String

1. In your Neon project dashboard, click "Connection Details"
2. Copy the connection string (it looks like):
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```
3. Keep this secure - it contains your database credentials

## Step 4: Configure Backend Environment

1. Navigate to `project/backend/` directory
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` file and add your connection string:
   ```env
   DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars
   CORS_ORIGINS=http://localhost:3000
   HOST=0.0.0.0
   PORT=8000
   ENVIRONMENT=development
   ```

4. Generate a secure secret for `BETTER_AUTH_SECRET`:
   ```bash
   # On Linux/Mac:
   openssl rand -base64 32

   # On Windows (PowerShell):
   [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
   ```

## Step 5: Create Database Tables

1. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

2. Install dependencies (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

3. Create tables by running the application once:
   ```bash
   uvicorn app.main:app --reload
   ```

   The SQLModel tables will be created automatically on first run.

4. Verify tables were created:
   - Go to Neon console
   - Click "Tables" in sidebar
   - You should see: `users` and `tasks` tables

## Step 6: Verify Database Connection

1. Check backend logs for successful connection:
   ```
   INFO:     Application startup complete.
   ```

2. Test health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

   Should return:
   ```json
   {"status": "healthy"}
   ```

## Step 7: Run Backend Tests

1. Run all tests:
   ```bash
   pytest
   ```

2. Run specific test suites:
   ```bash
   # Authentication tests
   pytest tests/test_auth.py -v

   # Task tests
   pytest tests/test_tasks.py -v
   ```

3. Run with coverage:
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

## Step 8: Configure Frontend Environment

1. Navigate to `project/frontend/` directory
2. Copy `.env.local.example` to `.env.local`:
   ```bash
   cp .env.local.example .env.local
   ```

3. Edit `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=same-secret-as-backend
   BETTER_AUTH_URL=http://localhost:3000
   ```

## Step 9: Start Both Servers

1. **Terminal 1 - Backend**:
   ```bash
   cd project/backend
   venv\Scripts\activate  # Windows
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Terminal 2 - Frontend**:
   ```bash
   cd project/frontend
   npm run dev
   ```

## Step 10: Test the Application

1. Open browser to [http://localhost:3000](http://localhost:3000)

2. **Test Authentication**:
   - Click "Sign Up"
   - Create account with email and password
   - Verify redirect to tasks page
   - Sign out and sign in again

3. **Test Task Management**:
   - Create a new task
   - Mark task as complete
   - Edit task title and description
   - Delete task (with confirmation)
   - Test filtering (All, Pending, Completed)

4. **Test User Isolation**:
   - Create second user account
   - Verify each user only sees their own tasks
   - Verify cannot access other user's tasks via API

## Troubleshooting

### Connection Refused
- Verify DATABASE_URL is correct
- Check Neon project is active (not paused)
- Verify SSL mode is included: `?sslmode=require`

### Authentication Errors
- Verify BETTER_AUTH_SECRET matches between frontend and backend
- Check secret is at least 32 characters
- Clear browser localStorage and try again

### CORS Errors
- Verify CORS_ORIGINS includes frontend URL
- Check frontend is running on correct port (3000)
- Restart backend after changing CORS settings

### Table Not Found
- Run backend once to create tables
- Check Neon console to verify tables exist
- Verify DATABASE_URL points to correct database

### Tests Failing
- Ensure database is accessible
- Check test database is separate from development
- Verify all dependencies are installed

## Database Schema

### users table
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    name VARCHAR,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### tasks table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

## Security Notes

1. **Never commit `.env` files** - They contain sensitive credentials
2. **Use strong secrets** - Minimum 32 characters for BETTER_AUTH_SECRET
3. **Enable SSL** - Always use `?sslmode=require` in production
4. **Rotate secrets** - Change BETTER_AUTH_SECRET periodically
5. **Limit CORS** - Only allow trusted frontend origins

## Next Steps

After database setup is complete:
1. Run full test suite to verify all functionality
2. Test all 6 user stories end-to-end
3. Proceed with Phase 9: Integration & Testing
4. Prepare for deployment (Phase 10)
5. Polish and documentation (Phase 11)

## Support

- **Neon Documentation**: [https://neon.tech/docs](https://neon.tech/docs)
- **FastAPI Documentation**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Next.js Documentation**: [https://nextjs.org/docs](https://nextjs.org/docs)
