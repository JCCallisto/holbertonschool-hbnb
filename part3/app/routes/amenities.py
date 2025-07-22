from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.extensions import db
from models.amenity import Amenity
from app.schemas.amenity_schema import AmenitySchema

amenities_bp = Blueprint('amenities_bp', __name__)
amenity_schema = AmenitySchema()
amenities_schema = AmenitySchema(many=True)

@amenities_bp.route('/', methods=['POST'])
@jwt_required()
def create_amenity():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = amenity_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    amenity = Amenity(**data)
    db.session.add(amenity)
    db.session.commit()
    return amenity_schema.dump(amenity), 201

@amenities_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_amenities():
    amenities = Amenity.query.all()
    return jsonify(amenities_schema.dump(amenities)), 200

@amenities_bp.route('/<int:amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = amenity_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    for key, value in data.items():
        setattr(amenity, key, value)
    db.session.commit()
    return amenity_schema.dump(amenity), 200

@amenities_bp.route('/<int:amenity_id>', methods=['DELETE'])
@jwt_required()
def delete_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id)
    db.session.delete(amenity)
    db.session.commit()
    return jsonify({"message": "Amenity deleted"}), 200
