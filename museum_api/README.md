# Museum Bot Backend API

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.115.13-green.svg)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0.41-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)

A comprehensive backend API for a museum support bot that provides self-help courses, registration, feedback management, experience sharing, and user history tracking across multiple social media platforms (Telegram and VK).

## 🚀 Overview

This project is a FastAPI-based backend service designed to support museum visitor engagement through interactive features. The API manages user registrations, delivers self-support courses, handles feedback, enables experience sharing, and tracks user history.

### Key Features

- **Multi-platform Support**: Works with both Telegram and VK bots
- **Self-Support Courses**: Structured educational content delivery system
- **User Registration**: Comprehensive user profile management
- **Feedback Management**: Collection and administration of user feedback
- **Experience Sharing**: Platform for users to share their museum experiences
- **User History Tracking**: Records user interactions and story consumption
- **Database Integration**: MySQL-powered persistence layer
- **Health Monitoring**: Built-in health checks and monitoring

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs with Python 3.7+
- **Database**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and Object-Relational Mapping system
- **Database**: [MySQL](https://www.mysql.com/) - Open-source relational database management system
- **Dependency Management**: [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management
- **Containerization**: [Docker](https://www.docker.com/) - Platform for developing and shipping applications
- **Monitoring**: [Sentry](https://sentry.io/) - Error tracking and performance monitoring

## 📋 Requirements

- Python 3.11 or higher
- MySQL 5.7 or higher
- Docker (optional, for containerized deployment)

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file based on the `env.example` file:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=museum_bot
DB_USER=museum_user
DB_PASSWORD=museum_password

# Application Configuration
APP_NAME=Museum Bot Backend
APP_VERSION=1.0.0
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# API Service Configuration
TG_BOT_API_BASE_URL=http://help-museum_bot:9000
VK_BOT_API_BASE_URL=http://help-vk_bot:9001

# Sentry Configuration (optional)
SENTRY_DSN=https://your-sentry-dsn@errors.asarta.ru/12
SENTRY_ENVIRONMENT=development

# Optional: Complete database URL (alternative to individual DB_* variables)
# DATABASE_URL=mysql+pymysql://user:password@localhost:3306/museum_bot
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | Database host |
| `DB_PORT` | 3306 | Database port |
| `DB_NAME` | museum_bot | Database name |
| `DB_USER` | museum_user | Database username |
| `DB_PASSWORD` | museum_password | Database password |
| `APP_NAME` | Museum Bot Backend | Application name |
| `APP_VERSION` | 1.0.0 | Application version |
| `DEBUG` | true | Enable debug mode |
| `HOST` | 0.0.0.0 | Host to bind to |
| `PORT` | 8000 | Port to listen on |
| `TG_BOT_API_BASE_URL` | http://help-museum_bot:9000 | Telegram bot API service URL |
| `VK_BOT_API_BASE_URL` | http://help-vk_bot:9001 | VK bot API service URL |
| `SENTRY_DSN` | https://your-sentry-dsn@errors.asarta.ru/12 | Sentry DSN for error tracking (optional) |
| `SENTRY_ENVIRONMENT` | development | Sentry environment setting |
| `DATABASE_URL` | mysql+pymysql://user:password@localhost:3306/museum_bot | Complete database connection string (alternative to individual DB_* variables) |

### API Endpoints

#### Health Check
```bash
GET /health
```
Response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### User Registration
```bash
POST /registration/register
Content-Type: application/json

{
  "sm_type": "tg",
  "telegram_id": "123456789",
  "tg_username": "username",
  "firstname": "John",
  "lastname": "Doe",
  "is_museum_worker": false,
  "museum": "Local Museum",
  "occupation": "Visitor"
}
```

#### Get Self-Support Course
```bash
GET /self_support_course/get_course/{course_id}?user_id=123
```

#### Submit Feedback
```bash
POST /feedback/incoming
Content-Type: application/json

{
  "sm_id": "123456789",
  "feedback": "Great experience at the museum!"
}
```

#### Share Experience
```bash
POST /share_experience/create
Content-Type: application/json

{
  "user_id": "123456789",
  "title": "Amazing Art Exhibition",
  "text": "Visited the museum today and was impressed...",
  "tag": ["art", "exhibition"],
  "is_anonymous": false,
  "is_agreed_to_publication": true
}
```

## 📚 API Documentation

The API is organized into several modules:

### Registration Module
Handles user registration and profile management across social media platforms.

- `POST /registration/register` - Register a new user
- `GET /registration/profile/{sm_id}` - Get user profile by social media ID

### Self-Support Course Module
Delivers structured educational content to users.

- `GET /self_support_course/get_course/{course_id}` - Retrieve course information
- `GET /self_support_course/get_part/{part_id}` - Get specific course part
- `POST /self_support_course/beginner` - Start beginner course
- `POST /self_support_course/answer` - Submit answer to course question

### Feedback Module
Manages collection and administration of user feedback.

- `POST /feedback/incoming` - Submit feedback
- `GET /feedback/list` - Get list of feedback entries
- `POST /feedback/answer` - Respond to feedback

### Share Experience Module
Enables users to share their museum experiences.

- `POST /share_experience/create` - Create new experience story
- `GET /share_experience/list` - Get list of published stories
- `GET /share_experience/{story_id}` - Get specific story

### History Module
Tracks user interactions and story consumption.

- `POST /history/add` - Add story to user history
- `GET /history/list/{user_id}` - Get user's history

### Common Module
Provides general utility endpoints.

- `GET /common/stats` - Get application statistics

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Issues
- Ensure MySQL server is running
- Verify database credentials in `.env` file
- Check that the database name exists
- Confirm network connectivity to database server

#### API Service Communication
- Verify that TG_BOT_API_BASE_URL and VK_BOT_API_BASE_URL are accessible
- Check that the bot services are running and responding
- Confirm network connectivity between services

#### Docker Issues
- Ensure Docker daemon is running
- Check that ports are available
- Verify Dockerfile permissions

#### Startup Issues
- Check Python version compatibility (requires 3.11+)
- Verify all dependencies are installed
- Review error logs for specific issue details

### Debugging Tips

1. Check application logs for error details
2. Verify environment variables are properly set
3. Test database connectivity separately
4. Use health check endpoint to verify basic functionality
5. Enable DEBUG mode for more verbose logging

## 🏗️ Project Structure

```
museum_api/
├── main.py                 # Main FastAPI application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .dockerignore          # Docker ignore rules
├── .gitignore             # Git ignore rules
├── env.example            # Environment variable template
├── init.sql               # Database initialization script
├── db/                    # Database-related modules
│   ├── database.py        # Database connection and session management
│   ├── models.py          # SQLAlchemy ORM models
│   └── utils.py           # Database utilities
├── modules/               # Feature modules
│   ├── common/            # Common utilities and endpoints
│   ├── feedback/          # Feedback management
│   ├── history/           # User history tracking
│   ├── registration/      # User registration
│   ├── self_support_course/ # Self-support courses
│   └── share_experience/  # Experience sharing
├── services/              # External service integrations
│   ├── tg_bot_api_service/ # Telegram bot integration
│   └── vk_bot_api_service/ # VK bot integration
└── shared/                # Shared models and utilities
    └── models.py          # Shared Pydantic models
```

## 🎯 Modules Overview

### Registration Module
Handles user registration across social media platforms (Telegram/VK) with comprehensive profile information including name, role (visitor/museum worker), and museum affiliation.

### Self-Support Course Module
Provides a structured learning experience with courses divided into parts, each with titles, descriptions, videos, images, and interactive questions. Tracks user progress and collects answers.

### Feedback Module
Enables users to submit feedback through social media channels and provides an administrative interface for managing and responding to feedback.

### Share Experience Module
Allows users to share their museum experiences through stories with titles, content, tags, and privacy options.

### History Module
Tracks which stories users have viewed to prevent duplicate exposure and enable personalized recommendations.