# Museum Ideas Project - Docker Setup

This project contains a museum bot system with a FastAPI backend and a Telegram bot frontend, all containerized with Docker.

## Architecture

- **MySQL Database**: Stores application data
- **FastAPI Backend**: REST API for the museum bot functionality
- **Telegram Bot**: AI-powered bot built with aiogram

## Prerequisites

- Docker and Docker Compose installed
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

## Quick Start

1. **Clone the repository and navigate to the project directory**

2. **Set up environment variables**
   ```bash
   # Copy the environment template
   cp env.example .env
   
   # Edit .env and add your Telegram bot token
   # BOT_TOKEN=your_actual_bot_token_here
   ```

3. **Build and start all services**
   ```bash
   docker-compose up -d
   ```

4. **Check service status**
   ```bash
   docker-compose ps
   ```

5. **View logs**
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f museum_api
   docker-compose logs -f museum_bot
   docker-compose logs -f mysql
   ```

## Services

### MySQL Database
- **Port**: 3306
- **Database**: museum_bot
- **User**: museum_user
- **Password**: museum_password
- **Root Password**: rootpassword

### FastAPI Backend
- **Port**: 8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

### Telegram Bot
- **Depends on**: FastAPI backend
- **Environment**: Requires BOT_TOKEN

## Development

### Running in Development Mode
The services are configured with volume mounts for development:

```bash
# Start services with live code reloading
docker-compose up -d

# Make changes to your code and they'll be reflected immediately
# (FastAPI will auto-reload, bot will need restart for changes)
```

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete database data)
docker-compose down -v
```

### Rebuilding Services
```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build museum_api
docker-compose build museum_bot
```

## Database Management

### Access MySQL
```bash
# Connect to MySQL container
docker-compose exec mysql mysql -u museum_user -p museum_bot

# Or as root
docker-compose exec mysql mysql -u root -p
```

### Database Migrations
The FastAPI service includes Alembic for database migrations:

```bash
# Run migrations
docker-compose exec museum_api alembic upgrade head

# Create new migration
docker-compose exec museum_api alembic revision --autogenerate -m "description"
```

## Troubleshooting

### Common Issues

1. **Bot not starting**: Check if BOT_TOKEN is set correctly in .env
2. **Database connection issues**: Ensure MySQL is healthy before starting API
3. **Port conflicts**: Change ports in docker-compose.yml if needed

### Health Checks
```bash
# Check service health
docker-compose ps

# View health check logs
docker inspect museum_api | grep -A 10 Health
```

### Logs and Debugging
```bash
# View real-time logs
docker-compose logs -f --tail=100

# Access container shell
docker-compose exec museum_api bash
docker-compose exec museum_bot bash
```

## Production Deployment

For production deployment:

1. **Security**: Change default passwords in docker-compose.yml
2. **Environment**: Use proper .env file with production values
3. **Volumes**: Consider using named volumes for data persistence
4. **Networks**: Configure proper network security
5. **Monitoring**: Add monitoring and logging solutions

## File Structure

```
museum_ideas/
├── docker-compose.yml          # Main Docker Compose configuration
├── env.example                 # Environment variables template
├── README.md                   # This file
├── museum_api/                 # FastAPI backend
│   ├── Dockerfile             # API container configuration
│   ├── requirements.txt       # Python dependencies
│   ├── main.py               # FastAPI application
│   └── ...
├── museum_bot/                # Telegram bot
│   ├── Dockerfile            # Bot container configuration
│   ├── requirements.txt      # Python dependencies
│   ├── main.py              # Bot application
│   └── ...
└── ...
```

## Contributing

1. Make changes to your code
2. Test locally with Docker Compose
3. Commit your changes
4. Submit a pull request

## License

[Add your license information here] 