from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON body"}), 400

    email = (data.get('email') or '').strip().lower()
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email or not password or not first_name or not last_name:
        return jsonify({"msg": "Email, password, first_name, and last_name are required"}), 400

    existing_user = User.query.filter(func.lower(User.email) == email).first()
    if existing_user:
        return jsonify({"msg": "Email already registered"}), 400

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Email already registered"}), 400

    return jsonify(user.to_dict()), 201

@users_bp.route('/api/v1/users/', methods=['GET'])
@jwt_required()
def list_users():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Forbidden"}), 403
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@users_bp.route('/api/v1/users/<string:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Forbidden"}), 403
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@users_bp.route('/api/v1/users/<string:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user_id_from_token = get_jwt_identity()
    claims = get_jwt()
    user = User.query.get_or_404(user_id)
    # Only admin or the user themself can update
    if not claims.get('is_admin') and str(user.id) != str(user_id_from_token):
        return jsonify({"msg": "Forbidden"}), 403
    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    if claims.get('is_admin'):
        email = data.get('email')
        if email:
            if User.query.filter(func.lower(User.email) == email.lower(), User.id != user.id).first():
                return jsonify({"msg": "Email already taken"}), 400
            user.email = email
        password = data.get('password')
        if password:
            user.set_password(password)
        is_admin = data.get('is_admin')
        if is_admin is not None:
            user.is_admin = bool(is_admin)
    db.session.commit()
    return jsonify({"msg": "User updated"}), 200

@users_bp.route('/api/v1/users/<string:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Forbidden"}), 403
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200
