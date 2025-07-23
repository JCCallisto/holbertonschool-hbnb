from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.place import Place
from app.models.amenity import Amenity
from flask_jwt_extended import jwt_required, get_jwt_identity

place_amenities_bp = Blueprint('place_amenities', __name__)

@place_amenities_bp.route('/api/v1/places/<int:place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    place = Place.query.get_or_404(place_id)
    return jsonify([{"id": a.id, "name": a.name, "description": a.description} for a in place.amenities]), 200

@place_amenities_bp.route('/api/v1/places/<int:place_id>/amenities', methods=['POST'])
@jwt_required()
def add_amenity_to_place(place_id):
    place = Place.query.get_or_404(place_id)
    current_user = get_jwt_identity()
    if place.owner_id != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"msg": "Forbidden"}), 403
    data = request.get_json()
    amenity_id = data.get('amenity_id')
    amenity = Amenity.query.get_or_404(amenity_id)
    if amenity not in place.amenities:
        place.amenities.append(amenity)
        db.session.commit()
    return jsonify({"msg": "Amenity added to place"}), 200

@place_amenities_bp.route('/api/v1/places/<int:place_id>/amenities/<int:amenity_id>', methods=['DELETE'])
@jwt_required()
def remove_amenity_from_place(place_id, amenity_id):
    place = Place.query.get_or_404(place_id)
    current_user = get_jwt_identity()
    if place.owner_id != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"msg": "Forbidden"}), 403
    amenity = Amenity.query.get_or_404(amenity_id)
    if amenity in place.amenities:
        place.amenities.remove(amenity)
        db.session.commit()
    return jsonify({"msg": "Amenity removed from place"}), 200
