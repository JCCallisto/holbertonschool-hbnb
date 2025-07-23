from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.place import Place
from flask_jwt_extended import jwt_required, get_jwt_identity

places_bp = Blueprint('places', __name__)

@places_bp.route('/api/v1/places/', methods=['POST'])
@jwt_required()
def create_place():
    current_user = get_jwt_identity()
    data = request.get_json()
    place = Place(name=data['name'], description=data.get('description'), owner_id=current_user['id'])
    db.session.add(place)
    db.session.commit()
    return jsonify({"id": place.id, "name": place.name}), 201

@places_bp.route('/api/v1/places/', methods=['GET'])
def get_places():
    places = Place.query.all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description, "owner_id": p.owner_id} for p in places]), 200

@places_bp.route('/api/v1/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get_or_404(place_id)
    return jsonify({"id": place.id, "name": place.name, "description": place.description, "owner_id": place.owner_id}), 200

@places_bp.route('/api/v1/places/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    place = Place.query.get_or_404(place_id)
    current_user = get_jwt_identity()
    if place.owner_id != current_user['id'] and not current_user['is_admin']:
        return jsonify({"msg": "Forbidden"}), 403
    data = request.get_json()
    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)
    db.session.commit()
    return jsonify({"msg": "Place updated"}), 200

@places_bp.route('/api/v1/places/<int:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    place = Place.query.get_or_404(place_id)
    current_user = get_jwt_identity()
    if place.owner_id != current_user['id'] and not current_user['is_admin']:
        return jsonify({"msg": "Forbidden"}), 403
    db.session.delete(place)
    db.session.commit()
    return jsonify({"msg": "Place deleted"}), 200
