from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.review import Review
from app.models.place import Place
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/api/v1/reviews/', methods=['POST'])
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    place = Place.query.get_or_404(data['place_id'])
    user = User.query.get_or_404(current_user_id)
    # Prevent reviewing your own place
    if place.owner_id == current_user_id:
        return jsonify({"msg": "Cannot review your own place"}), 403
    # Prevent duplicate review
    existing_review = Review.query.filter_by(user_id=current_user_id, place_id=place.id).first()
    if existing_review:
        return jsonify({"msg": "Already reviewed this place"}), 400
    review = Review(
        text=data['text'],
        rating=data['rating'],
        user_id=current_user_id,
        place_id=place.id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"id": review.id, "text": review.text, "rating": review.rating}), 201

@reviews_bp.route('/api/v1/reviews/<string:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    current_user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    user = User.query.get_or_404(current_user_id)
    is_admin = user.is_admin if hasattr(user, "is_admin") else False
    if review.user_id != current_user_id and not is_admin:
        return jsonify({"msg": "Unauthorized action"}), 403
    data = request.get_json()
    review.text = data.get('text', review.text)
    review.rating = data.get('rating', review.rating)
    db.session.commit()
    return jsonify({"msg": "Review updated"}), 200

@reviews_bp.route('/api/v1/reviews/<string:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    user = User.query.get_or_404(current_user_id)
    is_admin = user.is_admin if hasattr(user, "is_admin") else False
    if review.user_id != current_user_id and not is_admin:
        return jsonify({"msg": "Unauthorized action"}), 403
    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review deleted"}), 200

@reviews_bp.route('/api/v1/places/<string:place_id>/reviews/', methods=['POST'])
@jwt_required()
def create_place_review(place_id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    place = Place.query.get_or_404(place_id)
    data = request.get_json()
    # Prevent reviewing your own place
    if place.owner_id == current_user_id:
        return jsonify({"msg": "Cannot review your own place"}), 403
    # Prevent duplicate review
    existing_review = Review.query.filter_by(user_id=current_user_id, place_id=place.id).first()
    if existing_review:
        return jsonify({"msg": "Already reviewed this place"}), 400
    review = Review(
        text=data['text'],
        rating=data['rating'],
        user_id=current_user_id,
        place_id=place.id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"id": review.id, "text": review.text, "rating": review.rating}), 201

@reviews_bp.route('/api/v1/places/<string:place_id>/reviews/', methods=['GET'])
def list_place_reviews(place_id):
    place = Place.query.get_or_404(place_id)
    reviews = Review.query.filter_by(place_id=place.id).all()
    return jsonify([{"id": r.id, "text": r.text, "rating": r.rating, "user_id": r.user_id} for r in reviews]), 200
