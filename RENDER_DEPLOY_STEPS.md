# 🚀 Deploy JobPilot AI on Render - EASY GUIDE

## ✅ Prerequisites Completed
- ✅ `render.yaml` created
- ✅ PostgreSQL support added to `requirements.txt`
- ✅ All code ready for deployment

---

## 📋 Step-by-Step Deployment (10 minutes)

### **STEP 1: Push Code to GitHub**

Open Command Prompt in your project folder and run:

```cmd
git init
git add .
git commit -m "Initial commit - JobPilot AI ready for deployment"
```

Now create a new repository on GitHub:
1. Go to https://github.com/new
2. Repository name: `jobpilot-ai`
3. Make it **Public** (required for free tier)
4. Click **"Create repository"**

Then push your code:

```cmd
git remote add origin https://github.com/YOUR_USERNAME/jobpilot-ai.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

### **STEP 2: Deploy on Render**

1. **Go to Render**: https://render.com/
2. **Sign Up/Login** with your GitHub account
3. Click **"New +"** button (top right)
4. Select **"Blueprint"**
5. Click **"Connect a repository"**
6. Find and select your `jobpilot-ai` repository
7. Render will auto-detect the `render.yaml` file
8. Click **"Apply"** 

Render will now create:
- ✅ Web service (your API + Dashboard)
- ✅ Worker service (background job scanner)
- ✅ PostgreSQL database (free 1GB)

---

### **STEP 3: Add Environment Variables**

After deployment starts, you need to add your secret environment variables:

#### **For Web Service:**

1. In Render dashboard, click on **"jobpilot-ai-web"**
2. Go to **"Environment"** tab on the left
3. Click **"Add Environment Variable"**
4. Add these one by one:

```
SMTP_USERNAME = chauhanpriya0460@gmail.com
SMTP_PASSWORD = wursvsoolpzvtoxn
NOTIFY_EMAIL_TO = chauhanpriya0460@gmail.com

WHATSAPP_ACCESS_TOKEN = EAARZAC0kuv2YBSAv0HDJhHieE8lHedtawQPHYORjZAp7u48FAEMAiAJdPuW8fEtWYEqxJiQHW1UH2ZB0ZCD7Eni6ITEhKwM2zVnGWxEeWk0jFQCrWKd26hSVZBrZBCCpxkHj71JBDBzfywy9WSFhiIyGH4YMPYiikIY1a9xOOl5014lavpqZC3k2oHodmDU9IewZALsSBJLCGhRrcPIuwBXJG4c2BFVQdZBbwrRHZAOjzXZAJ9DtTIIWw3lnYjtx5AtNmfjZADOxnTGvoa6TZCwVMAuZBmZAjJOkQZDZD
WHATSAPP_PHONE_NUMBER_ID = 1344464935407648
WHATSAPP_TO = 918126394481
```

5. Click **"Save Changes"**

#### **For Worker Service:**

1. Go back to dashboard
2. Click on **"jobpilot-ai-worker"**
3. Go to **"Environment"** tab
4. Add the **SAME** environment variables as above
5. Click **"Save Changes"**

**Note:** You need to add these to BOTH services!

---

### **STEP 4: Initialize Database**

After deployment completes:

1. In **jobpilot-ai-web** service
2. Click **"Shell"** tab (on the left)
3. Run this command:

```bash
python -m database.database
```

This creates the database tables.

---

### **STEP 5: Access Your App! 🎉**

Your app will be live at:

```
https://jobpilot-ai-web.onrender.com
```

You can find the exact URL in the Render dashboard at the top of your web service page.

---

## 🔍 Verify Everything Works

### **Check Web Service:**
1. Visit your URL: `https://jobpilot-ai-web.onrender.com`
2. You should see the beautiful dashboard
3. Check status shows "● Agent Online"

### **Check Worker Service:**
1. In Render dashboard, click **"jobpilot-ai-worker"**
2. Click **"Logs"** tab
3. You should see: `"Job scanner started. Scanning every 20 minutes..."`

### **Test Notifications:**
- Wait 20 minutes for first scan, OR
- Run manual scan from the Shell tab:
  ```bash
  python -m worker.scheduler
  ```

---

## 💰 Render Free Tier Limits

✅ **What's Free:**
- 750 hours/month of web service
- 750 hours/month of worker service
- 1GB PostgreSQL database
- Automatic HTTPS
- Auto-deploy on git push

⚠️ **Limitations:**
- Services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Background worker may need to be kept alive

---

## 🚀 Keep Worker Running 24/7 (Optional)

Free tier workers can sleep. To keep it running:

**Option 1: Upgrade to Paid ($7/month)**
- In worker service, upgrade to "Starter" plan
- Worker stays running 24/7

**Option 2: Use Cron Job (Free)**
- Use a service like [cron-job.org](https://cron-job.org)
- Ping your web service every 10 minutes
- This keeps the web service awake

---

## 🔄 Update Your Deployment

Anytime you make code changes:

```cmd
git add .
git commit -m "Your change description"
git push
```

Render will **automatically redeploy**! 🎉

---

## 🆘 Troubleshooting

### **Build Failed?**
- Check the build logs in Render
- Make sure all files are committed to git
- Verify `requirements.txt` is correct

### **Database Connection Error?**
- Make sure you ran `python -m database.database` in the Shell
- Check if DATABASE_URL is set (Render does this automatically)

### **Worker Not Running?**
- Check worker service logs
- Make sure environment variables are set in BOTH services
- Verify no errors in the logs

### **WhatsApp Not Working?**
- Token expires every 24-48 hours
- Generate new token and update in Render environment variables
- Click "Save Changes" to restart service

### **Web Service Shows "Service Unavailable"?**
- It's probably sleeping (free tier)
- Wait 30 seconds and refresh
- Or upgrade to paid plan ($7/month)

---

## 📞 Get Help

If something doesn't work:
1. Check the **Logs** tab in Render (very helpful!)
2. Make sure environment variables are set in BOTH services
3. Verify database was initialized

---

## 🎉 You're Done!

Your JobPilot AI is now:
- ✅ Live on the internet
- ✅ Scanning for jobs every 20 minutes
- ✅ Sending email notifications
- ✅ Sending WhatsApp notifications
- ✅ Accessible from anywhere

**Your Live URL:** `https://jobpilot-ai-web.onrender.com`

Share it with friends and start getting job opportunities! 🚀

---

## 💡 Next Steps

1. **Bookmark your URL**
2. **Star your GitHub repo** (to find it easily)
3. **Update profile** in `backend/profile.py` with your actual info
4. **Monitor notifications** - check your email and WhatsApp
5. **Consider upgrading** to paid plan ($7/month) for 24/7 operation

Good luck with your job search! 🎯
