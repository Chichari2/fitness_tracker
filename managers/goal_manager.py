from models import Goal, db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GoalManager:

    @staticmethod
    def create_goal(user_id, data):
        try:
            new_goal = Goal(
                user_id=user_id,
                name=data.get('activity_type', 'Unnamed Activity'),  # Используем activity_type как name
                value=data['target_value'],                           # Используем target_value как value
                start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),  # Преобразуем строку в дату
                end_date=datetime.strptime(data['end_date'], '%Y-%m-%d')       # Преобразуем строку в дату
            )
            db.session.add(new_goal)
            db.session.commit()
            return new_goal
        except Exception as e:
            logger.error(f"Error in create_goal: {str(e)}")
            db.session.rollback()
            raise

    @staticmethod
    def get_user_goals(user_id):
        try:
            return Goal.query.filter_by(user_id=user_id).all()
        except Exception as e:
            logger.error(f"Error fetching goals for user {user_id}: {str(e)}")
            raise

    @staticmethod
    def update_goal(user_id, goal_id, data):
        try:
            goal = Goal.query.filter_by(user_id=user_id, id=goal_id).first_or_404()

            if 'activity_type' in data:
                goal.name = data['activity_type']
            if 'target_value' in data:
                goal.value = data['target_value']
            if 'end_date' in data:
                goal.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

            goal.last_update_date = datetime.utcnow()
            db.session.commit()
            return goal
        except Exception as e:
            logger.error(f"Error in update_goal: {str(e)}")
            db.session.rollback()
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

