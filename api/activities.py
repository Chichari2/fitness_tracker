from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Activity, User
from models import db
from . import api_bp

@api_bp.route('/users/<int:user_id>/activities', methods=['GET'])
@jwt_required()
def get_user_activities(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    user = User.query.get_or_404(user_id)
    activities = Activity.query.filter_by(user_id=user.id).all()
    return jsonify([activity.to_dict() for activity in activities]), 200

@api_bp.route('/users/<int:user_id>/activities', methods=['POST'])
@jwt_required()
def add_user_activity(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    user = User.query.get_or_404(user_id)
    #
    data = request.get_json()
    new_activity = Activity(
        user_id=user.id,
        activity_type=data['activity_type'],
        duration_seconds=data['duration_seconds']
    )
    db.session.add(new_activity)
    db.session.commit()
    #
    return jsonify(new_activity.to_dict()), 201
