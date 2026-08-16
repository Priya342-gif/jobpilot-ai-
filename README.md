# JobPilot AI

An autonomous job-discovery and skill-gap assistant.

## Features

- Candidate profile based on a verified resume
- Job ingestion through permitted/public APIs
- Duplicate detection
- Skill matching
- Missing-skill analysis
- 20-minute background scanner
- Application tracking
- Email notification support
- WhatsApp Cloud API notification support
- Optional Playwright browser automation
- Simple web dashboard
- Auto-apply is OFF by default

## Important

The application agent must not:
- invent qualifications or experience
- submit false answers
- bypass CAPTCHA or anti-bot controls
- bypass login/security controls
- apply outside the rules configured by the candidate

## Setup

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Create the database:

```bash
python -m database.database
```

Run the API:

```bash
uvicorn backend.main:app --reload
```

Open:

http://127.0.0.1:8000

API docs:

http://127.0.0.1:8000/docs

Run the autonomous worker in another terminal:

```bash
python -m worker.scheduler
```

## Optional Playwright setup

```bash
playwright install chromium
```

Do not enable automatic application until you have tested the workflow and configured your application rules.


### 📄 Resume-Based Matching

The user's resume/profile acts as the basis for matching jobs.

The system can compare:

-   Programming languages
-   Frameworks and libraries
-   Embedded/IoT technologies
-   Machine-learning tools
-   Experience
-   Projects
-   Education
-   Other job requirements

### 🧠 Skill-Gap Analysis

For every relevant job, JobPilot can separate requirements into:

``` text
✅ Skills already present
❌ Skills missing from the profile
```

Example:

``` text
Job: Embedded Systems Intern
Match: 87%

Present:
✓ C/C++
✓ ESP32
✓ UART
✓ SPI

Missing:
✗ FreeRTOS
✗ CAN
```

The system can then notify the user that the missing skills are worth
learning or adding to their preparation plan.

> JobPilot should not falsely add qualifications to a resume. A missing
> skill should be reported as a skill gap rather than automatically
> claiming that the user possesses it.

### 📱 WhatsApp Notifications

JobPilot supports the **WhatsApp Cloud API** for sending job alerts and
skill-gap notifications.

Example:

``` text
🚨 New Job Match

Embedded Systems Intern
Match: 87%

Missing Skills:
• FreeRTOS
• CAN

Recommendation:
Learn/practice these skills before applying.

Application:
🔒 Approval required
```

### 📧 Email Notifications

Optional SMTP email notifications can be used alongside WhatsApp.

The project supports configurable SMTP settings through environment
variables.

### 🔒 Approval-Controlled Applications

Job discovery does **not** automatically mean job application.

The intended workflow is:

``` text
Job Found
   ↓
Analyze
   ↓
Notify User
   ↓
User Reviews
   ↓
Approve
   ↓
Application Workflow
```

This keeps the final application decision with the user.

### 💾 SQLite Database

The project includes a SQLite database (`jobpilot.db`) for
application/job data and state management.

SQLite keeps the initial deployment simple because it does not require a
separate database server.

For larger multi-user production deployments, a persistent production
database can be introduced later.

### 🌐 FastAPI Backend

The backend is built around FastAPI and exposes the application's API.

During local development, the API can be run with Uvicorn.

### 🐳 Docker Support

The repository includes Docker deployment support so the application can
be packaged consistently across environments.

### ☁️ Cloud Deployment

The project is designed to be deployable as a web service on cloud
platforms such as Render.

The deployment architecture separates the web/API service from the
long-running job-search worker when required.

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
                         ┌─────────────────┐
                         │      User       │
                         │ Resume/Profile  │
                         └────────┬────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │   Resume/Profile Data  │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │    JobPilot Scheduler  │
                     │     Every 20 Minutes   │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │     Job Discovery      │
                     │  APIs / Web Sources    │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │    Job Processing      │
                     │ Title / Description /  │
                     │ Requirements / URL     │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │   Resume ↔ Job Match   │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │    Skill Gap Agent     │
                     └────────────┬───────────┘
                                  │
                         ┌────────┴────────┐
                         ▼                 ▼
                  ┌─────────────┐   ┌─────────────┐
                  │  WhatsApp   │   │    Email    │
                  └──────┬──────┘   └──────┬──────┘
                         │                 │
                         └────────┬────────┘
                                  ▼
                           ┌─────────────┐
                           │    User     │
                           └──────┬──────┘
                                  │
                         ┌────────┴────────┐
                         ▼                 ▼
                      APPROVE            IGNORE
```

------------------------------------------------------------------------

# ⏱️ 20-Minute Automation

The intended autonomous loop is:

``` text
00:00  Search jobs
00:01  Collect job information
00:02  Remove previously processed jobs
00:03  Compare with profile
00:04  Calculate match
00:05  Identify skill gaps
00:06  Store results
00:07  Send notifications
...
00:20  Run again
```

The exact execution time depends on the configured worker and job-source
response time.

------------------------------------------------------------------------

# 📂 Project Structure

A typical project structure is:

``` text
jobpilot-ai-full/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   └── ...
│
├── database/
│   └── ...
│
├── worker/
│   └── scheduler.py
│
├── data/
│   └── jobpilot.db
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

> The exact structure may vary depending on the current implementation.

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Component            Technology
  -------------------- ------------------------------------
  Backend              FastAPI
  Server               Uvicorn
  Language             Python
  Database             SQLite
  Browser Automation   Playwright
  Notifications        WhatsApp Cloud API
  Email                SMTP
  Containerization     Docker
  Source Control       Git / GitHub
  Deployment           Render / compatible cloud platform
  Scheduler            Python worker

------------------------------------------------------------------------

# ⚙️ Local Installation

## 1. Clone the repository

``` bash
git clone https://github.com/YOUR_USERNAME/jobpilot-ai-full.git
cd jobpilot-ai-full
```

## 2. Create a virtual environment

### Windows

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

and then:

``` powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

``` powershell
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 🔐 Environment Variables

Create a local `.env` file based on `.env.example`.

Example structure:

``` env
# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
NOTIFY_EMAIL_TO=your-email@gmail.com

# WhatsApp Cloud API
WHATSAPP_ACCESS_TOKEN=your-meta-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_TO=your-whatsapp-number
```

### Security

**Never commit `.env` to GitHub.**

Make sure `.gitignore` contains:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
```

API tokens and passwords should be stored as environment variables or
cloud-platform secrets.

If an access token is accidentally exposed, revoke/rotate it
immediately.

------------------------------------------------------------------------

# 📱 WhatsApp Setup

JobPilot uses the Meta WhatsApp Cloud API.

The notification module sends a text message through the WhatsApp Graph
API.

The required configuration is:

``` env
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_TO=
```

A simple connection test can be run using the project's WhatsApp test
script if present:

``` powershell
.\.venv\Scripts\python.exe test_whatsapp.py
```

A successful result should indicate:

``` text
Success: True
```

------------------------------------------------------------------------

# 📧 Email Setup

For Gmail SMTP:

``` env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
NOTIFY_EMAIL_TO=your-email@gmail.com
```

Use a Gmail **App Password** rather than your normal Gmail password when
required by your account configuration.

------------------------------------------------------------------------

# ▶️ Running the API

Start the FastAPI application locally:

``` powershell
uvicorn backend.main:app --reload
```

Then open:

``` text
http://127.0.0.1:8000
```

FastAPI documentation is normally available at:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 🔄 Running the Worker

If the scheduler is implemented as the project's worker module:

``` powershell
python -m worker.scheduler
```

The worker is responsible for the recurring automation.

For production, run the worker separately from the web/API service when
the deployment platform supports multiple services.

------------------------------------------------------------------------

# 🐳 Docker

Build:

``` bash
docker build -t jobpilot-ai .
```

Run:

``` bash
docker run --env-file .env -p 8000:8000 jobpilot-ai
```

For Docker-based deployment, make sure the web server listens on:

``` text
0.0.0.0
```

and uses the hosting platform's assigned port where required.

------------------------------------------------------------------------

# ☁️ Render Deployment

JobPilot can be deployed as a Render Web Service.

Recommended configuration:

``` text
Runtime:
Python

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Add all required environment variables through Render's Environment
Variables section.

Do **not** upload `.env` to the repository.

After deployment, the service should provide a public URL similar to:

``` text
https://jobpilot-ai.onrender.com
```

FastAPI documentation can then be tested at:

``` text
https://jobpilot-ai.onrender.com/docs
```

------------------------------------------------------------------------

# 🔔 Notification Example

A notification can contain:

``` text
🚨 New Job Match

Role: Embedded Systems Intern
Company: Example Robotics
Location: Delhi / Remote

Match Score: 87%

✅ Matching Skills
• C/C++
• ESP32
• MQTT
• UART

❌ Missing Skills
• FreeRTOS
• CAN

Recommendation:
Focus on FreeRTOS and CAN before applying.

Application:
Approval Required
```

------------------------------------------------------------------------

# 🧠 Skill-Gap Philosophy

JobPilot should distinguish between:

**Known skill**

``` text
The resume/profile explicitly contains the skill.
```

and

**Missing skill**

``` text
The job requires the skill, but the current profile does not demonstrate it.
```

It should **never automatically invent qualifications**.

For example:

``` text
Job requires:
FreeRTOS

Resume:
No FreeRTOS experience found

Result:
❌ Missing Skill: FreeRTOS
```

not:

``` text
Resume:
FreeRTOS ✓
```

This makes the system useful for both job discovery and targeted
learning.

------------------------------------------------------------------------

# 🔒 Safety & User Control

JobPilot is designed around **human approval**.

The recommended workflow is:

``` text
Automatic:
✓ Search
✓ Analyze
✓ Match
✓ Detect skill gaps
✓ Notify

User controlled:
✓ Decide whether to apply
✓ Approve application
✓ Provide final information
```

The system should not submit applications without explicit user
authorization.

------------------------------------------------------------------------

# 📈 Future Improvements

Potential future features include:

-   Multi-user accounts
-   Resume version management
-   Job-source integrations
-   Better semantic job matching
-   AI-generated job summaries
-   Personalized learning plans
-   Application tracking
-   Interview preparation
-   Application history dashboard
-   PostgreSQL for production-scale persistence
-   Background task queue
-   Better duplicate detection
-   Analytics dashboard
-   Browser-based approval workflow
-   Role-specific resume recommendations

------------------------------------------------------------------------

# 🎯 Project Goal

JobPilot AI aims to turn job searching from a repetitive manual process
into an intelligent assistant:

``` text
MANUAL JOB SEARCH

Search → Read → Compare → Research Skills → Track → Repeat

                         ↓

                    JOBPILOT AI

Discover → Match → Find Skill Gaps → Notify → User Approves
```

The goal is not to replace the candidate's decision-making.

The goal is to **save time, surface relevant opportunities, identify
what to learn next, and keep the final application decision with the
candidate.**

------------------------------------------------------------------------

## 👨‍💻 Author

**Priya Chauhan**

B.Tech Artificial Intelligence and Machine Learning

GitHub: https://github.com/Priya342-gif

Email: chauhanpriya1926@gmail.com

------------------------------------------------------------------------

## ⭐ Project Status

**Status:** Active Development

The current project includes the core backend, notification
integrations, SQLite storage, Docker support, and deployment
configuration. Job-source integrations, production-scale persistence,
and some autonomous workflows may continue to evolve as development
progresses.
