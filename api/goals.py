from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Goal, User
from . import api_bp

@api_bp.route('/users/<int:user_id>/goals', methods=['GET'])
@jwt_required()
def get_user_goals(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    user = User.query.get_or_404(user_id)
    goals = Goal.query.filter_by(user_id=user.id).all()
    return jsonify([goal.to_dict() for goal in goals]), 200

@api_bp.route('/users/<int:user_id>/goals', methods=['POST'])
@jwt_required()
def add_user_goal(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        abort(403, description="Access forbidden")

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_goal = Goal(
        user_id=user.id,
        name=data['name'],
        value=data['value'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(new_goal.to_dict()), 201
