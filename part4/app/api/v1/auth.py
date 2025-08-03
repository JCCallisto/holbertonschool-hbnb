from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import create_access_token
from app.extensions import db
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON body"}), 400

    email = (data.get('email') or '').strip().lower()
    password = data.get('password')
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()

    # Validate input
    if not (email and password and first_name and last_name):
        return jsonify({"msg": "Missing required fields"}), 400

    # Check for existing user (case-insensitive)
    if User.query.filter(func.lower(User.email) == email).first():
        return jsonify({"msg": "Email already registered"}), 400

    # Create user
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)  # Assumes set_password hashes and sets the password

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Database error"}), 500

    return jsonify(user.to_dict()), 201

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Email and password required"}), 400
    user = User.query.filter_by(email=data['email'].lower().strip()).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401

    claims = {
        "email": user.email,
        "is_admin": user.is_admin
    }
    access_token = create_access_token(identity=str(user.id), additional_claims=claims)
    return jsonify(access_token=access_token), 200
