"""Configuration for VibeScape."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Image generation settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    IMAGE_MODEL = os.environ.get('IMAGE_MODEL', 'dall-e-3')
    IMAGE_SIZE = os.environ.get('IMAGE_SIZE', '1024x1024')
    IMAGE_QUALITY = os.environ.get('IMAGE_QUALITY', 'standard')
    
    # Slideshow settings
    SLIDESHOW_INTERVAL = int(os.environ.get('SLIDESHOW_INTERVAL', '60'))  # seconds
    CACHE_DIR = os.environ.get('CACHE_DIR', 'static/generated')
    MAX_CACHED_IMAGES = int(os.environ.get('MAX_CACHED_IMAGES', '20'))
    
    # Generation settings
    GENERATION_INTERVAL = int(os.environ.get('GENERATION_INTERVAL', '300'))  # seconds between generations
