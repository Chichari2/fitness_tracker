from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from models import db
from . import api_bp
from sqlalchemy.exc import IntegrityError


@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, description="Missing required fields")

    # Check IF users with the same username
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        abort(400, description="Username already taken")

    new_user = User(username=data['username'], email=data.get('email'))
    new_user.set_password(data['password'])

    try:
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return jsonify(access_token=access_token), 201
    except IntegrityError:
        # Rollback transaction in case of uniqueness error
        db.session.rollback()
        abort(500, description="An error occurred during registration")


@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user is None or not user.verify_password(data['password']):
        abort(401, description="Bad username or password")

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200
