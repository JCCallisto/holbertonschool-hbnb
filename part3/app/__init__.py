from flask import Flask, jsonify
from app.extensions import db
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError

def create_app(config_object='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt = JWTManager(app)

    from app.models.place_amenity import place_amenity
    from app.models.user import User
    from app.models.amenity import Amenity
    from app.models.review import Review
    from app.models.place import Place

    from app.routes.users import users_bp
    from app.routes.places import places_bp
    from app.routes.reviews import reviews_bp
    from app.routes.amenities import amenities_bp
    from app.routes.auth import auth_bp
    from app.routes.place_amenities import place_amenities_bp
    from app.routes.place_reviews import place_reviews_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(place_amenities_bp)
    app.register_blueprint(place_reviews_bp)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({"msg": "Database integrity error (likely duplicate field)"}), 400
     
    return app
