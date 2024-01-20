from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_name: str
    database_port: str
    database_host: str
    database_user: str
    database_password: str
    secret_key: str
    algorithm: str
    access_key_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()