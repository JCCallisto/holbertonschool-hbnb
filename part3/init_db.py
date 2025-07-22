from app import create_app
from app.extensions import db

# Use your config class (adjust if named differently)
app = create_app('app.config.DevelopmentConfig')

with app.app_context():
    db.create_all()
    print("Database tables created!")
