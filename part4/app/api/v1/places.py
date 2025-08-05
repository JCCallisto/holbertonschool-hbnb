from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import PlaceSchema

places_bp = Blueprint('places', __name__)
place_schema = PlaceSchema()

@places_bp.route('/api/v1/places/', methods=['GET'])
def get_places():
    places = Place.query.all()
    return jsonify([p.to_dict() for p in places]), 200

@places_bp.route('/api/v1/places/<string:place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get_or_404(place_id)
    # Build reviews list with user_name
    reviews = Review.query.filter_by(place_id=place.id).all()
    review_list = []
    for r in reviews:
        user = User.query.get(r.user_id)
        if user:
            first = user.first_name if user.first_name else ""
            last = user.last_name if user.last_name else ""
            user_name = (first + " " + last).strip() if (first or last) else user.email
        else:
            user_name = "Anonymous"
        review_list.append({
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user_id,
            "user_name": user_name
        })

    # Get place data and embed reviews
    place_data = place.to_dict()
    place_data['reviews'] = review_list
    return jsonify(place_data), 200

@places_bp.route('/api/v1/places/', methods=['POST'])
@jwt_required()
def create_place():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON body"}), 400
    try:
        validated = place_schema.load(data)
    except Exception as e:
        return jsonify({"msg": str(e)}), 400
    place = Place(
        name=validated['name'],
        description=validated.get('description'),
        price=validated['price'],
        latitude=validated.get('latitude'),
        longitude=validated.get('longitude'),
        location=validated.get('location'),
        owner_id=current_user
    )
    db.session.add(place)
    db.session.commit()
    return jsonify(place.to_dict()), 201

@places_bp.route('/api/v1/places/<string:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    current_user = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    if place.owner_id != current_user:
        return jsonify({"msg": "Unauthorized action"}), 403
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON body"}), 400
    try:
        validated = place_schema.load(data, partial=True)
    except Exception as e:
        return jsonify({"msg": str(e)}), 400
    for key, value in validated.items():
        setattr(place, key, value)
    db.session.commit()
    return jsonify({"msg": "Place updated"}), 200

@places_bp.route('/api/v1/places/<string:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    current_user = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    if place.owner_id != current_user:
        return jsonify({"msg": "Unauthorized action"}), 403
    db.session.delete(place)
    db.session.commit()
    return jsonify({"msg": "Place deleted"}), 200

@places_bp.route('/api/v1/places/search', methods=['GET'])
def search_places():
    location = request.args.get('location')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    query = Place.query
    if location:
        query = query.filter(Place.location.ilike(f'%{location}%'))
    if min_price is not None:
        query = query.filter(Place.price >= min_price)
    if max_price is not None:
        query = query.filter(Place.price <= max_price)
    places = query.all()
    return jsonify([p.to_dict() for p in places]), 200
