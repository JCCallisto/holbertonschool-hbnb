from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db, bcrypt, jwt

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.routes.users import users_bp
    from app.routes.auth import auth_bp
    from app.routes.places import places_bp
    from app.routes.reviews import reviews_bp
    from app.routes.amenities import amenities_bp

    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(places_bp, url_prefix='/api/v1/places')
    app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews')
    app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')

    return app
