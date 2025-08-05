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
    if not data or 'place_id' not in data or 'text' not in data or 'rating' not in data:
        return jsonify({"msg": "Missing required fields"}), 400
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
    first = user.first_name if user and user.first_name else ""
    last = user.last_name if user and user.last_name else ""
    user_name = (first + " " + last).strip() if (first or last) else user.email if user else "Anonymous"
    return jsonify({
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user_id,
        "user_name": user_name
    }), 201

@reviews_bp.route('/api/v1/reviews/<string:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    current_user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    user = User.query.get_or_404(current_user_id)
    is_admin = getattr(user, "is_admin", False)
    if review.user_id != current_user_id and not is_admin:
        return jsonify({"msg": "Unauthorized action"}), 403
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON body"}), 400
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
    is_admin = getattr(user, "is_admin", False)
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
    if not data or 'text' not in data or 'rating' not in data:
        return jsonify({"msg": "Missing required fields"}), 400
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
    first = user.first_name if user and user.first_name else ""
    last = user.last_name if user and user.last_name else ""
    user_name = (first + " " + last).strip() if (first or last) else user.email if user else "Anonymous"
    return jsonify({
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user_id,
        "user_name": user_name
    }), 201

@reviews_bp.route('/api/v1/places/<string:place_id>/reviews/', methods=['GET'])
def list_place_reviews(place_id):
    place = Place.query.get_or_404(place_id)
    reviews = Review.query.filter_by(place_id=place.id).all()
    review_list = []
    for r in reviews:
        user = User.query.get(r.user_id)
        # Debugging
        print(f"Review user_id: {r.user_id} --> user: {user.first_name if user else 'None'} {user.last_name if user else ''}")
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
    return jsonify(review_list), 200
