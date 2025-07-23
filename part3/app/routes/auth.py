from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity={"id": user.id, "is_admin": user.is_admin})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad credentials"}), 401
