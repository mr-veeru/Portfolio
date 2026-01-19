# Portfolio Website

A modern portfolio website built with Flask, showcasing projects, skills, and professional experience.

## Features

- Clean and responsive design
- Fast and lightweight Flask backend
- Rate limiting for API protection
- Compression for optimized performance
- Environment-based configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mr-veeru/Portfolio.git
cd Portfolio
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
Portfolio/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
├── .env.example           # Environment variables template
├── README.md              # Project documentation
├── src/                   # Source code package
│   ├── config.py          # Application configuration
│   ├── logger.py          # Logging configuration
│   └── routes/            # Route handlers
│       └── index.py       # Index and health check routes
├── static/                # Static files
│   ├── css/               # Stylesheets
│   │   └── portfolio.css  # Main stylesheet
│   └── js/                # JavaScript files
│       └── portfolio.js  # Main JavaScript file
└── templates/             # HTML templates
    └── index.html         # Homepage template
```

## Development

This project is in active development. More features and improvements are coming soon.

## Author

<div align="center">

**Veerendra Bannuru** - Backend Software Engineer

[![Email](https://img.shields.io/badge/Email-mr.veeru68@gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:mr.veeru68@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-@mr--veeru-181717?style=flat&logo=github&logoColor=white)](https://github.com/mr-veeru)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Veerendra-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/veerendra-bannuru-900934215)

---

**Built using Flask, HTML, CSS, and JavaScript**

</div>
