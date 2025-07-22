from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    is_admin = data.get('is_admin', False)

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 409

    user = User(email=email, first_name=first_name, last_name=last_name, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'is_admin': user.is_admin}), 201
