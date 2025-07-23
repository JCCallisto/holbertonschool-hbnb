from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.amenity import Amenity
from flask_jwt_extended import jwt_required, get_jwt_identity

amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/api/v1/amenities/', methods=['POST'])
@jwt_required()
def create_amenity():
    data = request.get_json()
    amenity = Amenity(name=data['name'], description=data.get('description'))
    db.session.add(amenity)
    db.session.commit()
    return jsonify({"id": amenity.id, "name": amenity.name}), 201

@amenities_bp.route('/api/v1/amenities/', methods=['GET'])
def get_amenities():
    amenities = Amenity.query.all()
    return jsonify([{"id": a.id, "name": a.name, "description": a.description} for a in amenities]), 200

@amenities_bp.route('/api/v1/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id)
    return jsonify({"id": amenity.id, "name": amenity.name, "description": amenity.description}), 200

@amenities_bp.route('/api/v1/amenities/<int:amenity_id>', methods=['PUT'])
@jwt_required()
def update_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id)
    data = request.get_json()
    amenity.name = data.get('name', amenity.name)
    amenity.description = data.get('description', amenity.description)
    db.session.commit()
    return jsonify({"msg": "Amenity updated"}), 200

@amenities_bp.route('/api/v1/amenities/<int:amenity_id>', methods=['DELETE'])
@jwt_required()
def delete_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id)
    db.session.delete(amenity)
    db.session.commit()
    return jsonify({"msg": "Amenity deleted"}), 200
