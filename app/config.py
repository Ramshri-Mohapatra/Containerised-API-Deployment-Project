from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file = ".env")
    
    app_name: str = "Task Manager API"
    app_version: str = "1.0.0"
    debug: bool = True

settings = Settings()