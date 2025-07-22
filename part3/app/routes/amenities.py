from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.extensions import db
from app.models.amenity import Amenity
from app.schemas.amenity_schema import AmenitySchema

amenities_bp = Blueprint('amenities_bp', __name__)
amenity_schema = AmenitySchema()
amenities_schema = AmenitySchema(many=True)

@amenities_bp.route('/', methods=['GET'])
def list_amenities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Amenity.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": amenities_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200
