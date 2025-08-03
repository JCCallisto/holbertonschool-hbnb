from app import create_app
from app.config import DevelopmentConfig

app = create_app("DevelopmentConfig")
