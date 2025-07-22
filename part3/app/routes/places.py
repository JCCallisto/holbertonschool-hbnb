from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from models.place import Place
from app.schemas.place_schema import PlaceSchema

places_bp = Blueprint('places_bp', __name__)
place_schema = PlaceSchema()
places_schema = PlaceSchema(many=True)

@places_bp.route('/', methods=['POST'])
@jwt_required()
def create_place():
    user_id = get_jwt_identity()
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = place_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    place = Place(**data, user_id=user_id)
    db.session.add(place)
    db.session.commit()
    return place_schema.dump(place), 201

@places_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_places():
    places = Place.query.all()
    return jsonify(places_schema.dump(places)), 200

@places_bp.route('/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    place = Place.query.get_or_404(place_id)
    user_id = get_jwt_identity()
    if place.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = place_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    for key, value in data.items():
        setattr(place, key, value)
    db.session.commit()
    return place_schema.dump(place), 200

@places_bp.route('/<int:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    place = Place.query.get_or_404(place_id)
    user_id = get_jwt_identity()
    if place.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(place)
    db.session.commit()
    return jsonify({"message": "Place deleted"}), 200
