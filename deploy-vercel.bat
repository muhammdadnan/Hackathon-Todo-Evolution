@echo off
echo ========================================
echo Phase 2 - Vercel Deployment Script
echo ========================================
echo.
echo This will deploy your Next.js app to Vercel
echo.
echo What you need to do:
echo 1. Authenticate in the browser (will open automatically)
echo 2. Answer a few simple questions
echo 3. Wait 2-3 minutes for deployment
echo.
echo Press any key to start deployment...
pause > nul

cd /d "%~dp0project\frontend"

echo.
echo Starting Vercel deployment...
echo.

npx vercel --prod

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Copy your deployment URL from above
echo Format: https://phase-2-todo-app-xxx.vercel.app
echo.
echo Test with demo credentials:
echo Email: demo@example.com
echo Password: demo123
echo.
pause
