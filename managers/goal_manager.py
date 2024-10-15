from models import Goal, db
from datetime import datetime

class GoalManager:

    @staticmethod
    def create_goal(user_id, data):
        new_goal = Goal(
            user_id=user_id,
            name=data['name'],
            value=data['value'],
            start_date=datetime.utcnow(),  # Устанавливаем start_date
            end_date=data['end_date']
        )
        db.session.add(new_goal)
        db.session.commit()
        return new_goal

    @staticmethod
    def get_user_goals(user_id):
        return Goal.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_goal(user_id, goal_id, data):
        goal = Goal.query.filter_by(user_id=user_id, id=goal_id).first_or_404()

        # Обновляем данные цели
        if 'name' in data:
            goal.name = data['name']
        if 'value' in data:
            goal.value = data['value']
        if 'end_date' in data:
            goal.end_date = data['end_date']

        goal.last_update_date = datetime.utcnow()  # Устанавливаем last_update_date
        db.session.commit()
        return goal

    @staticmethod
    def update_goal_progress(goal_id, distance):
        """
        Метод для обновления прогресса цели.
        Добавляет к `last_value` пройденное расстояние в метрах (distance).
        """
        goal = Goal.query.get_or_404(goal_id)
        goal.last_value += distance  # Обновляем текущий прогресс
        goal.last_update_date = datetime.utcnow()  # Обновляем дату последнего изменения
        db.session.commit()

    @staticmethod
    def delete_goal(user_id, goal_id):
        goal = Goal.query.filter_by(user_id=user_id, id=goal_id).first_or_404()
        db.session.delete(goal)
        db.session.commit()
