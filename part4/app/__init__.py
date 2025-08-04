from flask import Flask
from app.extensions import db, migrate, bcrypt, jwt
from app.error_handlers import register_error_handlers
from app.api.v1.users import users_bp
from app.api.v1.places import places_bp
from app.api.v1.reviews import reviews_bp
from app.api.v1.auth import auth_bp
from app.api.v1.place_amenities import place_amenities_bp
from app.api.v1.place_reviews import place_reviews_bp
from app.api.v1.amenities import amenities_bp
from flask_cors import CORS  # <-- Import CORS

def create_app(config_class="DevelopmentConfig"):  # Default to development config
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_class}")
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    register_error_handlers(app)

    # Enable CORS for both localhost and 127.0.0.1 (frontend dev hosts)
    CORS(app, origins=["http://localhost:5500", "http://127.0.0.1:5500"])

    app.register_blueprint(users_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(place_amenities_bp)
    app.register_blueprint(place_reviews_bp)
    app.register_blueprint(amenities_bp)

    return app
