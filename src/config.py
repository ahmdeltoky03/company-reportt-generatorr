from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    cohere_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    agentops_api_key: Optional[str] = None
    
    app_name: str = "Company-Report-Generator"
    app_version: str = "0.1.0"
    debug: Optional[bool] = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
