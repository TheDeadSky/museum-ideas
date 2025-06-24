# Museum Bot Backend

A FastAPI-based backend for a museum bot application with MySQL database integration.

## Features

- FastAPI REST API
- MySQL database with SQLAlchemy ORM
- Docker containerization
- Environment-based configuration
- Database migrations with Alembic
- Health check endpoints

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

## Quick Start with Docker

1. **Clone the repository and navigate to the project directory**

2. **Start the application with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Local Development Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

4. **Start MySQL database:**
   ```bash
   docker-compose up db
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

## Database Configuration

The application uses MySQL with the following default configuration:

- **Host:** localhost (or `db` in Docker)
- **Port:** 3306
- **Database:** museum_bot
- **User:** museum_user
- **Password:** museum_password

### Environment Variables

Create a `.env` file based on `env.example`:

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
```

## Database Models

The application includes the following SQLAlchemy models:

- **User:** User information and authentication
- **Story:** User stories and content
- **UserQuestion:** Questions and answers
- **Course:** Educational courses
- **CoursePart:** Course sections and content
- **UserCourseProgress:** User progress tracking
- **StoryHistory:** Story viewing history

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check with database connectivity
- `GET /get-bot-text` - Retrieve bot text content
- `POST /begin-self-support-course` - Start a self-support course
- `POST /send-feedback` - Submit user feedback

## Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop services and remove volumes
docker-compose down -v

# Rebuild specific service
docker-compose build app
```

## Database Migrations

The project includes Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Development

### Project Structure

```
meuseum_bot_backend/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── schemas.py           # Pydantic models
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker services orchestration
├── init.sql            # Database initialization script
├── env.example         # Environment variables template
├── db/
│   ├── models.py       # SQLAlchemy models
│   └── database.py     # Database connection and session management
├── migrations/         # Alembic migrations
└── db_imitation/       # Mock data files
```

### Adding New Models

1. Define the model in `db/models.py`
2. Create and run migrations:
   ```bash
   alembic revision --autogenerate -m "Add new model"
   alembic upgrade head
   ```

### Adding New API Endpoints

1. Add the endpoint to `main.py`
2. Create corresponding Pydantic schemas in `schemas.py`
3. Add database operations using the `get_db` dependency

## Troubleshooting

### Database Connection Issues

1. Ensure MySQL is running and accessible
2. Check environment variables in `.env`
3. Verify database credentials
4. Check Docker network connectivity

### Docker Issues

1. Ensure Docker and Docker Compose are installed
2. Check if ports 8000 and 3306 are available
3. Rebuild containers: `docker-compose build --no-cache`

### Migration Issues

1. Check Alembic configuration in `alembic.ini`
2. Ensure database is accessible
3. Review migration files in `migrations/versions/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 