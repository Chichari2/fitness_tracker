from models import Goal, Activity, db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GoalManager:

    @staticmethod
    def create_goal(user_id, data):
        try:
            new_goal = Goal(
                user_id=user_id,
                name=data.get('activity_type', 'General Goal'),  # Default to "General Goal" if activity_type is missing
                value=data['target_value'],  # Use target_value from request
                start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
                end_date=datetime.strptime(data['end_date'], '%Y-%m-%d')
            )
            db.session.add(new_goal)
            db.session.commit()
            return new_goal
        except Exception as e:
            logger.error(f"Error in create_goal: {str(e)}")
            db.session.rollback()
            raise

    @staticmethod
    def get_user_goal(user_id):
        try:
            return Goal.query.filter_by(user_id=user_id).first()  # Only one goal per user
        except Exception as e:
            logger.error(f"Error fetching goal for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def calculate_goal_progress(user_id, goal_value):
        try:
            total_distance = db.session.query(db.func.sum(Activity.distance_meters)).filter_by(user_id=user_id).scalar()
            if total_distance is None:
                total_distance = 0
            return round((total_distance / goal_value) * 100, 2)
        except Exception as e:
            logger.error(f"Error calculating progress for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def delete_goal(user_id, goal_id):
        try:
            goal = Goal.query.filter_by(user_id=user_id, id=goal_id).first_or_404()
            db.session.delete(goal)
            db.session.commit()
        except Exception as e:
            logger.error(f"Error in delete_goal: {str(e)}")
            db.session.rollback()
            raise
