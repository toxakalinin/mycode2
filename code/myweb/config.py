import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    DEBUG = False
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
