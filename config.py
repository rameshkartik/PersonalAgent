"""
Configuration management for the Vector DB storage layer.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration settings."""
    
    # Vector DB Settings
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_data")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "personal_info")
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"


config = Config()
