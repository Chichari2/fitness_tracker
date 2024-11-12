
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from . import api_bp
from managers.activity_manager import ActivityManager

@api_bp.route('/users/<int:user_id>/activities', methods=['GET'])
@jwt_required()
def get_user_activities(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    activities = ActivityManager.get_user_activities(user_id)
    return jsonify([activity.to_dict() for activity in activities]), 200

@api_bp.route('/users/<int:user_id>/activities', methods=['POST'])
@jwt_required()
def add_user_activity(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_activity = ActivityManager.create_activity(user.id, data)
    return jsonify({
        "activity_id": new_activity.id,
        **new_activity.to_dict()
    }), 201

@api_bp.route('/users/<int:user_id>/activities/<int:activity_id>', methods=['PUT'])
@jwt_required()
def update_activity(user_id, activity_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    data = request.get_json()
    updated_activity = ActivityManager.update_activity(user_id, activity_id, data)
    return jsonify(updated_activity.to_dict()), 200

@api_bp.route('/users/<int:user_id>/activities/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(user_id, activity_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    ActivityManager.delete_activity(user_id, activity_id)
    return jsonify({"message": "Activity deleted"}), 200

@api_bp.route('/users/<int:user_id>/activities/<int:activity_id>/finish', methods=['POST'])
@jwt_required()
def finish_activity(user_id, activity_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    data = request.get_json()
    distance_meters = data.get('distance_meters')

    if distance_meters is None:
        abort(400, description="Distance is required to finish the activity.")

    finished_activity = ActivityManager.finish_activity(user_id, activity_id, distance_meters)
    return jsonify(finished_activity.to_dict()), 200
