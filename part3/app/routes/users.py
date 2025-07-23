from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/v1/users/', methods=['POST'])
def register():
    data = request.get_json()
    # Defensive: check that data is not None
    if not data:
        return jsonify({"msg": "Missing JSON body"}), 400

    email = (data.get('email') or '').strip().lower()
    password = data.get('password')
    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Use func.lower for case-insensitive check
    existing_user = User.query.filter(func.lower(User.email) == email).first()
    if existing_user:
        return jsonify({"msg": "Email already registered"}), 400

    user = User(
        email=email,
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:   # Catches duplicate constraint violation
        db.session.rollback()
        return jsonify({"msg": "Email already registered"}), 400

    return jsonify({"id": user.id, "email": user.email}), 201
