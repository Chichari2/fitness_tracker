# users.py
from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from . import api_bp
from managers.user_manager import UserManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        new_user = UserManager.create_user(data)
        access_token = create_access_token(identity=new_user.id)
        return jsonify({
            "access_token": access_token,
            "user_id": new_user.id
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        # Проверяем, что данные существуют и содержат email и password
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required"}), 400

        # Поменяли на поиск по email
        user = UserManager.authenticate_user(data['email'], data['password'])
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    except ValueError as e:
        logger.warning(f"Authentication failed: {str(e)}")
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
