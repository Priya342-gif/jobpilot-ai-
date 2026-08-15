# JobPilot AI - Running Locally ✅

## 🎉 Project is Now Running!

Your JobPilot AI application is successfully running on your local machine.

## 📍 Important Links

### Main Application
🌐 **Dashboard (Frontend)**: http://127.0.0.1:8000
- This is the main web interface where you can view jobs, matches, and skill gaps

### API Documentation
📚 **FastAPI Interactive Docs (Swagger UI)**: http://127.0.0.1:8000/docs
- Interactive API documentation where you can test all endpoints

📋 **Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc
- Alternative documentation format

### API Endpoints
You can test these directly in your browser or with tools like Postman:

- **Health Check**: http://127.0.0.1:8000/api/health
- **View Profile**: http://127.0.0.1:8000/api/profile
- **View Jobs**: http://127.0.0.1:8000/api/jobs
- **View Applications**: http://127.0.0.1:8000/api/applications

## 🏃 Running the Background Worker

To start the autonomous job search worker (runs every 20 minutes), open a NEW terminal and run:

```bash
cd c:\Users\HP\Downloads\jobpilot-ai-full-main\jobpilot-ai-full-main
.venv\Scripts\activate
python -m worker.scheduler
```

This will start the background automation that:
- Searches for jobs automatically
- Matches them with your profile
- Analyzes skill gaps
- Sends notifications (WhatsApp/Email)

## ⚙️ Configuration

Your environment variables are configured in `.env` file:
- **Auto Apply**: OFF (safe mode - requires manual approval)
- **Scan Interval**: 20 minutes
- **Min Match Score**: 70%
- **WhatsApp Notifications**: Configured
- **Email Notifications**: Needs SMTP password setup

## 🔧 Optional: Setup Playwright Browser Automation

If you want to use browser automation features:

```bash
.venv\Scripts\activate
playwright install chromium
```

## 📝 Quick Test

Test if the API is working:
1. Open http://127.0.0.1:8000/api/health in your browser
2. You should see JSON response with status information

## 🛑 Stopping the Server

To stop the FastAPI server:
- Press `CTRL+C` in the terminal where uvicorn is running

## 📱 Next Steps

1. ✅ Server is running
2. Configure your resume/profile data
3. Start the background worker (optional)
4. Set up WhatsApp/Email notifications (optional)
5. Test job matching with demo endpoints

## 🐛 Troubleshooting

- **Port already in use?** Use: `uvicorn backend.main:app --reload --port 8001`
- **Database errors?** Run: `python -m database.database` again
- **Module not found?** Make sure virtual environment is activated: `.venv\Scripts\activate`

---

**Author**: Ayush Pandey
**GitHub**: https://github.com/aayuk003
