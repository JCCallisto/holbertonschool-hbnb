from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/', methods=['POST'])
def register():
    data = request.get_json()
    user = User(email=data['email'], first_name=data.get('first_name'), last_name=data.get('last_name'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email}), 201

@users_bp.route('/api/v1/users/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email} for u in users]), 200

@users_bp.route('/api/v1/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name}), 200

@users_bp.route('/api/v1/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    current_user = get_jwt_identity()
    # Only allow user to update own info or admins
    if current_user['id'] != user.id and not current_user['is_admin']:
        return jsonify({"msg": "Forbidden"}), 403
    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    db.session.commit()
    return jsonify({"msg": "User updated"}), 200

@users_bp.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_user = get_jwt_identity()
    if current_user['id'] != user.id and not current_user['is_admin']:
        return jsonify({"msg": "Forbidden"}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200
