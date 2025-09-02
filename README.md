# HealthLinkAI - MindWell

##pitch deck link [ https://www.canva.com/design/DAGx0cn4Jzs/oi3GMA8_P-EeI5GpS0Wbrw/edit?utm_content=DAGx0cn4Jzs&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton ]
demo video [ https://drive.google.com/file/d/1bW0t37c6mDQHvovh5SAjLlkV2DYMvJa9/view?usp=drive_link ]


A comprehensive AI-powered health platform that provides symptom checking, mental health support, and healthcare provider connections.

## Features

- **AI Symptom Checker**: Analyze symptoms with AI-powered risk assessment
- **MindWell Support**: 24/7 mental health companion with crisis resources
- **Provider Network**: Find and connect with healthcare professionals
- **Health Dashboard**: Personalized health insights and recommendations
- **Responsive Design**: Modern UI with Tailwind CSS and accessibility features

## Tech Stack

- **Backend**: Flask, SQLAlchemy, MySQL
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **AI/ML**: Custom symptom analysis and mental health support engines
- **Database**: MySQL with Redis for caching
- **Deployment**: Docker, Gunicorn, Heroku-ready

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Redis (optional, for caching)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd healthlinkai
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

5. **Initialize database**
   ```bash
   # Create tables and admin user
   python app.py --init-db
   
   # Seed provider data (optional)
   python app.py --seed
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

### CLI Commands

The application includes built-in CLI commands:

```bash
# Initialize database (create tables + admin user)
python app.py --init-db

# Seed database with provider data
python app.py --seed

# Run development server (default)
python app.py
```

### Database Setup Options

#### Option 1: PlanetScale (Recommended - Free Tier Available)

1. **Create PlanetScale Account**
   - Go to [planetscale.com](https://planetscale.com)
   - Sign up for free account
   - Create new database (e.g., "healthlinkai")

2. **Get Connection String**
   - In PlanetScale dashboard, go to your database
   - Click "Connect" → "General" → "Python"
   - Copy the connection string (looks like):
   ```
   mysql+pymysql://username:password@host.planetscale.com/database?ssl=true
   ```

3. **Set Environment Variable**
   ```bash
   # In your .env file
   DATABASE_URL=mysql+pymysql://username:password@host.planetscale.com/database?ssl=true
   ```

#### Option 2: PythonAnywhere MySQL

1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://pythonanywhere.com)
   - Sign up for free account
   - Go to "Databases" tab

2. **Create MySQL Database**
   - Create database (e.g., "yourusername$healthlinkai")
   - Note your MySQL password

3. **Set Environment Variable**
   ```bash
   # In your .env file
   DATABASE_URL=mysql+pymysql://yourusername:password@yourusername.mysql.pythonanywhere-services.com/yourusername$healthlinkai
   ```

#### Option 3: Local MySQL (Development)

1. **Install MySQL locally**
2. **Create database**
   ```sql
   CREATE DATABASE healthlinkai;
   ```
3. **Set Environment Variable**
   ```bash
   # In your .env file
   DATABASE_URL=mysql+pymysql://root:password@localhost/healthlinkai
   ```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database (use one of the options above)
DATABASE_URL=mysql+pymysql://username:password@host/database?ssl=true

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

## Project Structure

```
healthlinkai/
├── backend/
│   ├── ai/                     # AI modules
│   │   ├── symptom_checker.py  # Symptom analysis engine
│   │   ├── mindwell_bot.py     # Mental health support bot
│   │   ├── recommend.py        # Recommendation engine
│   │   └── symptom_rules.json  # Symptom analysis rules
│   ├── static/                 # Static assets
│   │   ├── css/style.css       # Custom styles
│   │   ├── js/main.js          # JavaScript utilities
│   │   └── img/                # Images
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Homepage
│   │   ├── symptom_checker.html
│   │   ├── mindwell.html
│   │   ├── providers.html
│   │   └── dashboard.html
│   ├── tests/                  # Test suite
│   │   └── test_basic.py
│   ├── app.py                  # Flask application
│   ├── models.py               # Database models
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   ├── Dockerfile              # Docker configuration
│   ├── Procfile                # Heroku deployment
│   └── runtime.txt             # Python version
└── scripts/
    └── seed_providers.sql      # Database seed data
```

## API Endpoints

### Symptom Checker
```
POST /api/check-symptoms
Content-Type: application/json

{
  "symptoms": ["headache", "fever"],
  "age": 30,
  "gender": "female"
}
```

### MindWell Chat
```
POST /api/mindwell-chat
Content-Type: application/json

{
  "message": "I'm feeling anxious",
  "session_id": "unique_session_id"
}
```

### Recommendations
```
GET /api/recommendations
```

## Testing

Run the test suite:

```bash
cd backend
python -m pytest tests/ -v
```

Or run specific tests:

```bash
python tests/test_basic.py
```

## Deployment

### Docker

1. **Build the image**
   ```bash
   docker build -t healthlinkai .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 --env-file .env healthlinkai
   ```

### Heroku

1. **Install Heroku CLI and login**
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set DATABASE_URL=your-database-url
   heroku config:set SECRET_KEY=your-secret-key
   # Add other environment variables
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Production Considerations

- Use a production-grade database (PostgreSQL recommended)
- Set up Redis for caching and session storage
- Configure proper logging and monitoring
- Set up SSL/TLS certificates
- Implement rate limiting
- Set up automated backups
- Configure error tracking (Sentry)

## Security Features

- SQL injection protection via SQLAlchemy ORM
- XSS protection with proper input sanitization
- CSRF protection (can be enabled)
- Secure session management
- Input validation and sanitization
- Medical disclaimer prominently displayed

## Medical Disclaimer

**Important**: This application provides educational information only and is not intended for medical diagnosis or treatment. In emergencies, contact local emergency services immediately (911 in the US). Always consult with qualified healthcare professionals for medical advice.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Write tests for new features
- Update documentation as needed
- Ensure accessibility compliance
- Test across different browsers and devices

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue on GitHub
- Email: support@healthlinkai.com
- Documentation: [Project Wiki](link-to-wiki)

## Acknowledgments

- Built with Flask and modern web technologies
- UI components inspired by healthcare design best practices
- AI capabilities powered by custom algorithms
- Icons from Heroicons
- Styling with Tailwind CSS

---

**Version**: 1.0.0  
**Last Updated**: September 2024  
**Maintainers**: HealthLinkAI Development Team
