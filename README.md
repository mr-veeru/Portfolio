# Portfolio Website

## Overview

A modern, full-stack portfolio website showcasing professional experience, projects, and technical expertise. Built with Flask backend and vanilla JavaScript frontend, featuring clean architecture, RESTful APIs, and responsive design. Demonstrates professional backend development practices with proper separation of concerns and production-ready features.

**Live Site:** [https://veeru.pythonanywhere.com/](https://veeru.pythonanywhere.com/)

## Features

**Backend Architecture**
- Clean layered architecture (routes, services, data, models)
- RESTful API endpoints for dynamic content
- Rate limiting and security best practices
- Comprehensive error handling and logging
- Environment-based configuration
- SMTP email service for contact submissions

**Frontend Experience**
- Modern dark theme with gradient accents
- Fully responsive design
- Smooth animations and interactive elements
- Dynamic content loading via API
- Accessible navigation and keyboard support
- Optimized performance

**Developer Experience**
- Type hints throughout the codebase
- Comprehensive documentation and docstrings
- Clear project structure and naming conventions
- Easy configuration via environment variables

## Technology Stack

**Backend**
- Flask 3.0.0 - Web framework
- Python 3.10+ - Programming language
- Flask-Limiter - Rate limiting
- Email-Validator - Input validation

**Frontend**
- Vanilla JavaScript - No framework dependencies
- Modern CSS with custom properties
- HTML5 semantic markup
- Font Awesome icons

## Project Structure

```
Portfolio/
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
│
├── src/                        # Source code
│   ├── config.py               # Configuration management
│   ├── logger.py               # Logging setup
│   ├── exceptions.py           # Custom exceptions
│   ├── extensions.py           # Flask extensions
│   │
│   ├── routes/                 # HTTP endpoints
│   │   ├── index.py            # Homepage routes
│   │   ├── contact.py          # Contact form handler
│   │   └── api.py              # RESTful API endpoints
│   │
│   ├── services/               # Business logic
│   │   └── email_service.py    # Email sending service
│   │
│   ├── data/                   # Data access layer
│   │   └── data.py             # Portfolio data definitions
│   │
│   └── models/                 # Data models
│       ├── models.py           # Domain models
│       └── serializers.py      # Model serialization
│
├── static/                     # Static assets
│   ├── css/
│   │   └── portfolio.css       # stylesheet
│   ├── js/
│   │   └── portfolio.js        # Frontend logic
│   └── documents/              # Resume and profile image
│
└── templates/                  # HTML templates
    └── index.html              # Single-page application
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mr-veeru/Portfolio.git
   cd Portfolio
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```
   
   **Key environment variables:**
   - `FLASK_ENV` - Environment mode (development/production)
   - `SECRET_KEY` - Flask secret key for sessions
   - `SMTP_SERVER`, `SMTP_PORT` - Email server configuration
   - `SMTP_USERNAME`, `SMTP_PASSWORD` - Email credentials
   - `RECIPIENT_EMAIL` - Contact form recipient
   - `RATE_LIMIT_DEFAULTS` - API rate limiting configuration
   
   See `.env.example` for all available options.

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## API Endpoints

- `GET /api/projects` - Retrieve all projects
- `GET /api/skills` - Get skills organized by category
- `GET /api/experience` - Fetch professional experience
- `GET /api/education` - Get education history
- `GET /api/certifications` - Retrieve certifications
- `GET /api/stats` - Portfolio statistics

All endpoints return JSON responses with consistent structure.

## Architecture & Design

**Design Principles**
- Single Responsibility Principle - Each module has a clear purpose
- Separation of Concerns - Routes, services, and data layers are distinct
- DRY (Don't Repeat Yourself) - Reusable components and utilities
- Type Safety - Comprehensive type hints throughout

**Security & Performance**
- Rate limiting on contact form submissions
- Input validation and sanitization
- Email validation using industry-standard libraries
- Efficient data serialization
- Optimized CSS and JavaScript
- Lazy loading for images
- Minimal dependencies


## Development

### Running in Development Mode

The application runs in debug mode by default when `FLASK_ENV=development`. This enables:
- Auto-reload on code changes
- Detailed error messages
- Console logging

### Production Deployment

This application is deployed on PythonAnywhere. For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

**General deployment steps:**
1. Configure environment variables (see Installation step 4)
2. Set `FLASK_ENV=production` and a strong `SECRET_KEY`
3. Set up production logging
4. Use a production WSGI server (e.g., Gunicorn)
5. Configure reverse proxy (e.g., Nginx)

## Contributing

This is a personal portfolio project. However, suggestions and feedback are welcome!

## Author

**Veerendra Bannuru**

Backend Software Engineer with 2+ years of experience building scalable web applications and RESTful APIs. Specialized in Python, Flask, and modern software engineering practices.

**Connect:**
- Email: [mr.veeru68@gmail.com](mailto:mr.veeru68@gmail.com)
- GitHub: [@mr-veeru](https://github.com/mr-veeru)
- LinkedIn: [Veerendra Bannuru](https://www.linkedin.com/in/veerendra-bannuru-900934215)
