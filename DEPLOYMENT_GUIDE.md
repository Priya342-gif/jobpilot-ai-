# 🚀 JobPilot AI - Deployment Guide

Complete guide to deploy JobPilot AI to production.

---

## 📋 **Table of Contents**

1. [Quick Deploy - Render (Easiest)](#render-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [Railway Deployment](#railway-deployment)
5. [VPS/DigitalOcean Deployment](#vps-deployment)
6. [Environment Variables Setup](#environment-variables)

---

## 🎯 **OPTION 1: Render (Recommended - FREE Tier Available)**

### **Why Render?**
- ✅ Free tier available
- ✅ Easy to set up (5 minutes)
- ✅ Automatic HTTPS
- ✅ Background workers supported
- ✅ PostgreSQL database included

### **Step-by-Step:**

#### **1. Prepare Your Code**

Make sure these files exist in your project:

**`requirements.txt`** - Already exists ✅

**`render.yaml`** - Create this file:

```yaml
services:
  # Web Service (API + Dashboard)
  - type: web
    name: jobpilot-ai-web
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: APP_NAME
        value: JobPilot AI
      - key: DATABASE_URL
        fromDatabase:
          name: jobpilot-db
          property: connectionString
      - key: SCAN_INTERVAL_MINUTES
        value: 20
      - key: MIN_MATCH_SCORE
        value: 30
      - key: AUTO_APPLY
        value: false
      - key: SMTP_HOST
        value: smtp.gmail.com
      - key: SMTP_PORT
        value: 587
      - key: SMTP_USERNAME
        sync: false
      - key: SMTP_PASSWORD
        sync: false
      - key: NOTIFY_EMAIL_TO
        sync: false
      - key: WHATSAPP_ACCESS_TOKEN
        sync: false
      - key: WHATSAPP_PHONE_NUMBER_ID
        sync: false
      - key: WHATSAPP_TO
        sync: false
      - key: REMOTIVE_API_URL
        value: https://remotive.com/api/remote-jobs

  # Worker Service (Background Job Scanner)
  - type: worker
    name: jobpilot-ai-worker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m worker.scheduler
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: jobpilot-db
          property: connectionString
      - key: SCAN_INTERVAL_MINUTES
        value: 20
      - key: MIN_MATCH_SCORE
        value: 30
      - key: SMTP_HOST
        value: smtp.gmail.com
      - key: SMTP_PORT
        value: 587
      - key: SMTP_USERNAME
        sync: false
      - key: SMTP_PASSWORD
        sync: false
      - key: NOTIFY_EMAIL_TO
        sync: false
      - key: WHATSAPP_ACCESS_TOKEN
        sync: false
      - key: WHATSAPP_PHONE_NUMBER_ID
        sync: false
      - key: WHATSAPP_TO
        sync: false

databases:
  - name: jobpilot-db
    databaseName: jobpilot
    user: jobpilot
```

#### **2. Push to GitHub**

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - JobPilot AI"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/jobpilot-ai.git
git branch -M main
git push -u origin main
```

#### **3. Deploy on Render**

1. Go to https://render.com/
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml`
6. Click **"Apply"**

#### **4. Add Environment Variables**

In Render dashboard:
1. Go to **jobpilot-ai-web** service
2. Click **Environment**
3. Add these secrets:

```
SMTP_USERNAME = chauhanpriya0460@gmail.com
SMTP_PASSWORD = wursvsoolpzvtoxn
NOTIFY_EMAIL_TO = chauhanpriya0460@gmail.com

WHATSAPP_ACCESS_TOKEN = [your-token]
WHATSAPP_PHONE_NUMBER_ID = 1344464935407648
WHATSAPP_TO = 918126394481
```

4. Do the same for **jobpilot-ai-worker** service

#### **5. Access Your App**

Your app will be at: `https://jobpilot-ai-web.onrender.com`

---

## 🐳 **OPTION 2: Docker Deployment**

### **Step 1: Update Dockerfile**

Your `Dockerfile` already exists. Verify it has:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Step 2: Update docker-compose.yml**

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://jobpilot:password@db:5432/jobpilot
      - SCAN_INTERVAL_MINUTES=20
      - MIN_MATCH_SCORE=30
      - AUTO_APPLY=false
      - SMTP_HOST=smtp.gmail.com
      - SMTP_PORT=587
      - SMTP_USERNAME=${SMTP_USERNAME}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
      - NOTIFY_EMAIL_TO=${NOTIFY_EMAIL_TO}
      - WHATSAPP_ACCESS_TOKEN=${WHATSAPP_ACCESS_TOKEN}
      - WHATSAPP_PHONE_NUMBER_ID=${WHATSAPP_PHONE_NUMBER_ID}
      - WHATSAPP_TO=${WHATSAPP_TO}
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  worker:
    build: .
    command: python -m worker.scheduler
    environment:
      - DATABASE_URL=postgresql://jobpilot:password@db:5432/jobpilot
      - SCAN_INTERVAL_MINUTES=20
      - MIN_MATCH_SCORE=30
      - SMTP_HOST=smtp.gmail.com
      - SMTP_PORT=587
      - SMTP_USERNAME=${SMTP_USERNAME}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
      - NOTIFY_EMAIL_TO=${NOTIFY_EMAIL_TO}
      - WHATSAPP_ACCESS_TOKEN=${WHATSAPP_ACCESS_TOKEN}
      - WHATSAPP_PHONE_NUMBER_ID=${WHATSAPP_PHONE_NUMBER_ID}
      - WHATSAPP_TO=${WHATSAPP_TO}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=jobpilot
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=jobpilot
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### **Step 3: Deploy**

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🟣 **OPTION 3: Heroku Deployment**

### **Step 1: Install Heroku CLI**

```bash
# Windows
winget install Heroku.HerokuCLI

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### **Step 2: Create Procfile**

Create `Procfile` in root:

```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
worker: python -m worker.scheduler
```

### **Step 3: Create runtime.txt**

```
python-3.11.0
```

### **Step 4: Deploy**

```bash
# Login to Heroku
heroku login

# Create app
heroku create jobpilot-ai

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Set environment variables
heroku config:set SMTP_USERNAME=chauhanpriya0460@gmail.com
heroku config:set SMTP_PASSWORD=wursvsoolpzvtoxn
heroku config:set NOTIFY_EMAIL_TO=chauhanpriya0460@gmail.com
heroku config:set WHATSAPP_ACCESS_TOKEN=your-token
heroku config:set WHATSAPP_PHONE_NUMBER_ID=1344464935407648
heroku config:set WHATSAPP_TO=918126394481
heroku config:set MIN_MATCH_SCORE=30
heroku config:set SCAN_INTERVAL_MINUTES=20

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1

# Open app
heroku open
```

---

## 🚂 **OPTION 4: Railway Deployment**

### **Easiest Option!**

1. Go to https://railway.app/
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects Python
6. Add environment variables in dashboard
7. Deploy automatically!

**Railway provides:**
- ✅ Free $5 credit monthly
- ✅ PostgreSQL included
- ✅ Automatic HTTPS
- ✅ Easy setup

---

## 💻 **OPTION 5: VPS/DigitalOcean Deployment**

### **For Ubuntu/Debian VPS:**

#### **1. SSH into Server**

```bash
ssh root@your-server-ip
```

#### **2. Install Dependencies**

```bash
# Update system
apt update && apt upgrade -y

# Install Python
apt install python3 python3-pip python3-venv nginx -y

# Install PostgreSQL
apt install postgresql postgresql-contrib -y
```

#### **3. Setup Database**

```bash
sudo -u postgres psql

CREATE DATABASE jobpilot;
CREATE USER jobpilot WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE jobpilot TO jobpilot;
\q
```

#### **4. Clone and Setup Project**

```bash
cd /var/www
git clone https://github.com/YOUR_USERNAME/jobpilot-ai.git
cd jobpilot-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# (Add your environment variables)
```

#### **5. Setup Systemd Services**

**Web Service:** `/etc/systemd/system/jobpilot-web.service`

```ini
[Unit]
Description=JobPilot AI Web Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/jobpilot-ai
Environment="PATH=/var/www/jobpilot-ai/venv/bin"
ExecStart=/var/www/jobpilot-ai/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Worker Service:** `/etc/systemd/system/jobpilot-worker.service`

```ini
[Unit]
Description=JobPilot AI Worker Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/jobpilot-ai
Environment="PATH=/var/www/jobpilot-ai/venv/bin"
ExecStart=/var/www/jobpilot-ai/venv/bin/python -m worker.scheduler
Restart=always

[Install]
WantedBy=multi-user.target
```

#### **6. Setup Nginx**

```bash
nano /etc/nginx/sites-available/jobpilot
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/jobpilot /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### **7. Start Services**

```bash
systemctl start jobpilot-web
systemctl start jobpilot-worker
systemctl enable jobpilot-web
systemctl enable jobpilot-worker

# Check status
systemctl status jobpilot-web
systemctl status jobpilot-worker
```

#### **8. Setup SSL (Optional)**

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## 🔐 **Environment Variables Setup**

### **Required Variables:**

```bash
# App Settings
APP_NAME=JobPilot AI
SCAN_INTERVAL_MINUTES=20
MIN_MATCH_SCORE=30
AUTO_APPLY=false

# Database (for production, use PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=chauhanpriya0460@gmail.com
SMTP_PASSWORD=wursvsoolpzvtoxn
NOTIFY_EMAIL_TO=chauhanpriya0460@gmail.com

# WhatsApp Notifications
WHATSAPP_ACCESS_TOKEN=your-token-here
WHATSAPP_PHONE_NUMBER_ID=1344464935407648
WHATSAPP_TO=918126394481

# Job Source
REMOTIVE_API_URL=https://remotive.com/api/remote-jobs
```

---

## 📊 **Deployment Comparison**

| Platform | Difficulty | Cost | Time | Best For |
|----------|-----------|------|------|----------|
| **Render** | Easy | Free-$7/mo | 10 min | Beginners |
| **Railway** | Very Easy | Free $5/mo | 5 min | Quick deploy |
| **Heroku** | Medium | $7-13/mo | 15 min | Established platform |
| **Docker** | Medium | Varies | 20 min | Any server |
| **VPS** | Hard | $5-20/mo | 30+ min | Full control |

---

## ✅ **Post-Deployment Checklist**

### **1. Verify Services**

- [ ] Web service is running
- [ ] Worker service is running
- [ ] Database is connected
- [ ] Can access dashboard

### **2. Test Notifications**

- [ ] Email notifications working
- [ ] WhatsApp notifications working
- [ ] Job scanning working

### **3. Monitor**

- [ ] Check logs regularly
- [ ] Monitor job discovery
- [ ] Watch for errors

### **4. Update Profile**

- [ ] Update `backend/profile.py` with your info
- [ ] Redeploy after changes

---

## 🆘 **Troubleshooting**

### **Worker Not Running?**

```bash
# Check logs
heroku logs --tail --dyno worker  # Heroku
docker-compose logs worker        # Docker
systemctl status jobpilot-worker  # VPS
```

### **Database Errors?**

```bash
# Run migrations
python -m database.database
```

### **WhatsApp Not Working?**

- Check token expiry
- Verify phone number format
- Ensure 2-Step verification

### **Email Not Working?**

- Check Gmail App Password
- Verify SMTP settings
- Test with test_email.py

---

## 🎯 **Quick Start Recommendation**

### **For Beginners: Use Railway**

1. Push to GitHub
2. Connect Railway to repo
3. Add environment variables
4. Deploy!

**Done in 5 minutes!** ✅

---

## 📞 **Need Help?**

- Check logs first
- Verify environment variables
- Test locally before deploying
- Use debug mode for issues

---

## 🎉 **You're Ready to Deploy!**

Choose your platform and follow the steps above. Your JobPilot AI will be live in minutes!

**Recommended**: Start with Railway or Render for easiest setup.

Good luck! 🚀
