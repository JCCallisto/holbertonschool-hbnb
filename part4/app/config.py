import os

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'dev-jwt-secret-key'

class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://user:password@localhost/hbnb_prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'prod-jwt-secret-key')