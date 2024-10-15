from flask import jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from . import api_bp
from managers.user_manager import UserManager


@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        new_user = UserManager.create_user(data)
        access_token = create_access_token(identity=new_user.id)
        return jsonify({
            "access_token": access_token,
            "user_id": new_user.id  # Возвращаем ID нового пользователя
        }), 201
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(500, description=str(e))



@api_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  try:
    user = UserManager.authenticate_user(data['username'], data['password'])
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
  except ValueError as e:
    abort(401, description=str(e))
