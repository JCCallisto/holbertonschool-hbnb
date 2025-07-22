from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from models.user import User
from app.schemas.user_schema import UserSchema

users_bp = Blueprint('users_bp', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/', methods=['POST'])
def create_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@users_bp.route('/', methods=['GET'])
@jwt_required(optional=True)
def list_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = get_jwt_identity()
    if user.id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        data = user_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.dump(user), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = get_jwt_identity()
    if user.id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
