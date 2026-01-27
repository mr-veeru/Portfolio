# PythonAnywhere Deployment Guide

**Live Site:** [https://veeru.pythonanywhere.com/](https://veeru.pythonanywhere.com/)

## Prerequisites

- PythonAnywhere account ([pythonanywhere.com](https://www.pythonanywhere.com))
- Python 3.11 (or 3.10)
- Git repository

## Deployment Steps

### 1. Clone Repository

```bash
cd ~
git clone https://github.com/mr-veeru/Portfolio.git
cd Portfolio
```

### 2. Create Web App

1. Go to **Web** tab → **Add a new web app**
2. Choose domain: `yourusername.pythonanywhere.com`
3. Select **Manual configuration**
4. Select **Python 3.11**

### 3. Install Dependencies

```bash
cd ~/Portfolio
pip3.11 install -r requirements.txt
```

### 4. Configure WSGI File

1. In **Web** tab, click **WSGI configuration file** link
2. Replace content with:

```python
import sys
import os

# Update this path to match your username
project_home = '/home/veeru/Portfolio'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables (or use PythonAnywhere's Environment variables feature)
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['SMTP_SERVER'] = 'smtp.gmail.com'
os.environ['SMTP_PORT'] = '587'
os.environ['SMTP_USERNAME'] = 'your-email@gmail.com'
os.environ['SMTP_PASSWORD'] = 'your-app-password'
os.environ['RECIPIENT_EMAIL'] = 'mr.veeru68@gmail.com'
os.environ['LOG_LEVEL'] = 'INFO'
os.environ['RATE_LIMIT_DEFAULTS'] = '100 per day'
os.environ['RATE_LIMIT_STORAGE_URI'] = 'memory://'

from app import app as application
```

**Important:** 
- Replace `/home/veeru/Portfolio` with your actual path (e.g., `/home/yourusername/Portfolio`)
- **Better approach**: Use PythonAnywhere's **Environment variables** feature in the Web tab instead of hardcoding in WSGI file

### 5. Configure Static Files

1. In **Web** tab, scroll to **Static files**
2. Add mapping:
   - **URL:** `/static/`
   - **Directory:** `/home/veeru/Portfolio/static/`

### 6. Reload and Verify

1. Click **Reload** button in **Web** tab
2. Visit: `https://yourusername.pythonanywhere.com`
3. Test contact form and health endpoint

## Updating Deployment

```bash
cd ~/Portfolio
git pull
pip3.11 install -r requirements.txt
```

Then reload in **Web** tab.

## Troubleshooting

- **Import errors:** Verify dependencies installed with `pip3.11 install -r requirements.txt`
- **500 errors:** Check **Error log** in **Web** tab
- **Static files not loading:** Verify static file mapping path is correct
- **Module not found:** Install missing packages with `pip3.11 install package-name`

## Security Notes

- Never commit `.env` file or secrets
- **Recommended**: Use PythonAnywhere's **Environment variables** feature in Web tab for sensitive data (better than WSGI file)
- Generate strong `SECRET_KEY` for production
- Use Gmail App Password (not regular password) for SMTP
- PythonAnywhere free tier may block SMTP ports - consider using HTTP-based email service if needed

## PythonAnywhere-Specific Notes

- **Free tier limitations**: SMTP ports (587/465) may be blocked
- **Environment variables**: Prefer using Web tab → Environment variables over WSGI file
- **Logs location**: Check **Error log** in Web tab for debugging
- **HTTPS**: Automatically enabled on `*.pythonanywhere.com` domains
- **Rate limiting**: Memory storage works, but Redis not available on free tier
