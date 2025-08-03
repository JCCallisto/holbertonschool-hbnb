from flask import Blueprint, jsonify
from app.models.place import Place

place_reviews_bp = Blueprint('place_reviews', __name__)

@place_reviews_bp.route('/api/v1/places/<string:place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    place = Place.query.get_or_404(place_id)
    reviews = place.reviews
    return jsonify([{
        "id": r.id,
        "text": r.text,
        "rating": r.rating,
        "user_id": r.user_id  # Assuming Review has user_id not author_id
    } for r in reviews]), 200
