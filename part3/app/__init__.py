from flask import Flask
from app.extensions import db, jwt, migrate

def create_app(config_class='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes.users import users_bp
    from app.routes.places import places_bp
    from app.routes.reviews import reviews_bp
    from app.routes.amenities import amenities_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)

    return app
