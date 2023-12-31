from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    DEVENV: bool = False
    
    DATABASE_SCHEMA: str
    DATABASE_USER: str 
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    
    MONGO_INITDB_DATABASE: str
    
    DATABASE_URL: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    CLIENT_ORIGIN: str
    
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr

settings = Settings()
