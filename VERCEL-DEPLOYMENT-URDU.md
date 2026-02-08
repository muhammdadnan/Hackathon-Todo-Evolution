# Vercel Deployment Guide (Urdu/English)

## Tareeqa 1: Vercel Dashboard (Sabse Aasan - 5 Minutes)

### Step 1: Vercel Account Banao
1. Jao: https://vercel.com/signup
2. "Continue with GitHub" click karo
3. GitHub se login karo

### Step 2: Project Import Karo
1. Vercel dashboard kholo: https://vercel.com/new
2. "Import Git Repository" click karo
3. Apna repository select karo: "Hackathon-Todo-Evolution"
4. Ya direct link use karo: https://github.com/muhammdadnan/Hackathon-Todo-Evolution

### Step 3: Configuration
**Root Directory:** `project/frontend`

**Environment Variables (Zaroori!):**
- Name: `NEXT_PUBLIC_USE_MOCK_DATA`
- Value: `true`

### Step 4: Deploy
1. "Deploy" button click karo
2. 2-3 minutes wait karo
3. Deployment URL copy karo

### Step 5: Test Karo
- URL kholo browser mein
- Login karo: demo@example.com / demo123
- Sab features test karo

---

## Tareeqa 2: Vercel CLI (Terminal Se)

### Step 1: Vercel CLI Install Karo (Optional)
```bash
npm install -g vercel
```

### Step 2: Login Karo
```bash
vercel login
# Browser khulega, login karo
```

### Step 3: Deploy Karo
```bash
cd "C:\development-file\Hackaton-2\Phase-2 - clone\project\frontend"
vercel --prod
```

### Step 4: Questions Ka Jawab Do
```
? Set up and deploy? [Y/n] Y
? Which scope? [Select your account]
? Link to existing project? [y/N] N
? What's your project's name? hackathon-todo-evolution
? In which directory is your code located? ./
? Want to override the settings? [y/N] N
```

### Step 5: Environment Variable Add Karo
```bash
vercel env add NEXT_PUBLIC_USE_MOCK_DATA
# Value: true
# Environment: Production
```

### Step 6: Redeploy Karo
```bash
vercel --prod
```

---

## Demo Credentials
```
Email: demo@example.com
Password: demo123
```

---

## Agar Problem Aaye

### Build Error
- Check: Environment variable sahi hai?
- Check: Root directory `project/frontend` hai?

### 404 Error
- Root directory check karo
- Vercel dashboard mein settings dekho

### Environment Variable Missing
- Vercel dashboard → Settings → Environment Variables
- Add karo: NEXT_PUBLIC_USE_MOCK_DATA = true
- Redeploy karo

---

## Success Ke Baad

1. Deployment URL copy karo
2. Browser mein test karo
3. Demo credentials se login karo
4. Sab features check karo:
   - Task create
   - Task edit
   - Task complete
   - Task delete
   - AI Chat

---

## Deployment URL Format
```
https://hackathon-todo-evolution-xxx.vercel.app
```

Yeh URL apne hackathon submission mein use karo!
