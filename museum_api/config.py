from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/museum_bot"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "museum_bot"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    
    # Application settings
    APP_NAME: str = "Museum Bot Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        """Construct database URL from individual components"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Create settings instance
settings = Settings() 