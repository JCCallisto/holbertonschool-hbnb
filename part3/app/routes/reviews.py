from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.review import Review
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/api/v1/reviews/', methods=['POST'])
@jwt_required()
def create_review():
    current_user = get_jwt_identity()
    data = request.get_json()
    review = Review(
        text=data['text'],
        rating=data.get('rating'),
        place_id=data['place_id'],
        author_id=current_user['id']
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"id": review.id, "text": review.text, "rating": review.rating}), 201

@reviews_bp.route('/api/v1/reviews/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{
        "id": r.id, "text": r.text, "rating": r.rating,
        "place_id": r.place_id, "author_id": r.author_id
    } for r in reviews]), 200

@reviews_bp.route('/api/v1/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify({
        "id": review.id, "text": review.text, "rating": review.rating,
        "place_id": review.place_id, "author_id": review.author_id
    }), 200

@reviews_bp.route('/api/v1/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    current_user = get_jwt_identity()
    if review.author_id != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"msg": "Forbidden"}), 403
    data = request.get_json()
    review.text = data.get('text', review.text)
    review.rating = data.get('rating', review.rating)
    db.session.commit()
    return jsonify({"msg": "Review updated"}), 200

@reviews_bp.route('/api/v1/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    current_user = get_jwt_identity()
    if review.author_id != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"msg": "Forbidden"}), 403
    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review deleted"}), 200
