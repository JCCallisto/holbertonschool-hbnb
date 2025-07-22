from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.place import Place
from app.extensions import db

places_bp = Blueprint('places', __name__)

@places_bp.route('/api/v1/places/', methods=['POST'])
@jwt_required()
def create_place():
    current_user = get_jwt_identity()
    data = request.get_json()
    place = Place(name=data['name'], description=data.get('description'), owner_id=current_user['id'])
    db.session.add(place)
    db.session.commit()
    return jsonify({'id': place.id, 'name': place.name}), 201

@places_bp.route('/api/v1/places/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    current_user = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    if place.owner_id != current_user['id'] and not current_user['is_admin']:
        return jsonify({'msg': 'Forbidden'}), 403
    data = request.get_json()
    place.name = data.get('name', place.name)
    db.session.commit()
    return jsonify({'id': place.id, 'name': place.name}), 200
