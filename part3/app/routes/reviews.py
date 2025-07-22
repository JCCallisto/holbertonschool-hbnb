from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from models.review import Review
from app.schemas.review_schema import ReviewSchema

reviews_bp = Blueprint('reviews_bp', __name__)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = review_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    review = Review(**data, user_id=user_id)
    db.session.add(review)
    db.session.commit()
    return review_schema.dump(review), 201

@reviews_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_reviews():
    reviews = Review.query.all()
    return jsonify(reviews_schema.dump(reviews)), 200

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    user_id = get_jwt_identity()
    if review.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = review_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    for key, value in data.items():
        setattr(review, key, value)
    db.session.commit()
    return review_schema.dump(review), 200

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    user_id = get_jwt_identity()
    if review.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200
