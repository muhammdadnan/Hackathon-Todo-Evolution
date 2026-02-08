# Vercel CLI Deployment Commands

## ✅ Vercel CLI Installed: Version 50.13.2

## 🔐 Authentication Required

Aapko pehle login karna hoga. Main yeh nahi kar sakta.

### Step 1: Login Command
```bash
cd "C:\development-file\Hackaton-2\Phase-2 - clone\project\frontend"
vercel login
```

**Kya hoga:**
- Browser automatically khulega
- Vercel login page dikhega
- GitHub se login karo
- Terminal mein "Success!" dikhega

### Step 2: Deploy Command
```bash
vercel --prod
```

**Questions ka jawab:**
```
? Set up and deploy? Y
? Which scope? [Your account select karo]
? Link to existing project? N
? What's your project's name? hackathon-todo-evolution
? In which directory is your code located? ./
? Want to override the settings? N
```

### Step 3: Environment Variable
```bash
vercel env add NEXT_PUBLIC_USE_MOCK_DATA
```
**Value:** `true`
**Environment:** Production

### Step 4: Redeploy
```bash
vercel --prod
```

---

## 🚀 Complete Deployment Script

Yeh commands ek-ek karke run karo:

```bash
# 1. Frontend directory mein jao
cd "C:\development-file\Hackaton-2\Phase-2 - clone\project\frontend"

# 2. Login karo (browser khulega)
vercel login

# 3. Deploy karo
vercel --prod

# 4. Environment variable add karo
vercel env add NEXT_PUBLIC_USE_MOCK_DATA

# 5. Redeploy karo
vercel --prod
```

---

## 📋 Deployment Checklist

```
✅ Vercel CLI installed (v50.13.2)
⏳ Login required (aapko karna hai)
⏳ Deploy command (aapko run karna hai)
⏳ Environment variable (aapko add karna hai)
⏳ Final deployment (automatic hoga)
```

---

## 🎯 Expected Output

Deployment successful hone ke baad:
```
✅ Production: https://hackathon-todo-evolution-xxx.vercel.app [copied to clipboard]
```

---

## 🆘 Agar Problem Aaye

### "Not Authenticated"
```bash
vercel login
# Browser mein login karo
```

### "Build Failed"
```bash
# Environment variable check karo
vercel env ls
```

### "404 Error"
```bash
# Root directory check karo
# Ensure you're in: project/frontend
pwd
```

---

## ✅ Next Steps

1. **Terminal kholo** (Command Prompt ya PowerShell)
2. **Commands run karo** (upar diye gaye)
3. **Browser mein authenticate karo**
4. **Deployment URL copy karo**
5. **Test karo** (demo@example.com / demo123)

---

**Ready? Terminal kholo aur shuru karo!**
