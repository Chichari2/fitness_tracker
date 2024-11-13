from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from . import api_bp
from managers.goal_manager import GoalManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api_bp.route('/users/<int:user_id>/goals', methods=['GET'])
@jwt_required()
def get_user_goal(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    goal = GoalManager.get_user_goal(user_id)
    if not goal:
        return jsonify({"message": "No goal found for this user"}), 404

    goal_data = goal.to_dict()
    goal_data['progress'] = GoalManager.calculate_goal_progress(user_id, goal.value)
    return jsonify(goal_data), 200

@api_bp.route('/users/<int:user_id>/goals', methods=['POST'])
@jwt_required()
def add_user_goal(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    # Check if a distance goal already exists for the user
    existing_goal = GoalManager.get_user_goal(user_id)
    if existing_goal:
        return jsonify({"message": "User already has a distance goal"}), 400

    try:
        new_goal = GoalManager.create_goal(user.id, data)
        return jsonify(new_goal.to_dict()), 201
    except Exception as e:
        logger.error(f"Error creating goal: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@api_bp.route('/users/<int:user_id>/goals/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(user_id, goal_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    try:
        GoalManager.delete_goal(user_id, goal_id)
        return jsonify({"message": "Goal successfully deleted"}), 200
    except Exception as e:
        logger.error(f"Error deleting goal: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


