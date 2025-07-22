from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from app.models.review import Review
from app.schemas.review_schema import ReviewSchema

reviews_bp = Blueprint('reviews_bp', __name__)
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

@reviews_bp.route('/', methods=['GET'])
def list_reviews():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Review.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": reviews_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200
