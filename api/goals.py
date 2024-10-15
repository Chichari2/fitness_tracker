from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from . import api_bp
from managers.goal_manager import GoalManager

@api_bp.route('/users/<int:user_id>/goals', methods=['GET'])
@jwt_required()
def get_user_goals(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    goals = GoalManager.get_user_goals(user_id)
    return jsonify([goal.to_dict() for goal in goals]), 200

@api_bp.route('/users/<int:user_id>/goals', methods=['POST'])
@jwt_required()
def add_user_goal(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_goal = GoalManager.create_goal(user.id, data)
    return jsonify(new_goal.to_dict()), 201

# Маршрут для обновления цели
@api_bp.route('/users/<int:user_id>/goals/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(user_id, goal_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    data = request.get_json()
    updated_goal = GoalManager.update_goal(user_id, goal_id, data)
    return jsonify(updated_goal.to_dict()), 200

# Маршрут для удаления цели
@api_bp.route('/users/<int:user_id>/goals/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(user_id, goal_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    GoalManager.delete_goal(user_id, goal_id)
    return jsonify({"message": "Goal удалена успешно"}), 200
