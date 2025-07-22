from flask import Flask
from app.extensions import db, bcrypt, jwt
from app.routes.users import users_bp
from app.routes.auth import auth_bp
from app.routes.places import places_bp
from app.routes.amenities import amenities_bp
from app.routes.reviews import reviews_bp

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(reviews_bp)
    return app
