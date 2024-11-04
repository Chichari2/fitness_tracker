from models import Activity, Goal, db
from datetime import datetime
from flask import abort


class ActivityManager:

    @staticmethod
    def create_activity(user_id, data):
        # Создаем новую активность
        distance = data.get('distance_meters', 0)  # Получаем расстояние
        duration = data['duration_seconds']  # Получаем продолжительность

        average_speed = (distance / duration) * 3.6 if duration > 0 else 0  # Расчет средней скорости

        new_activity = Activity(
            user_id=user_id,
            goal_id=data.get('goal_id'),  # Привязываем к цели, если указана
            activity_type=data['activity_type'],
            duration_seconds=duration,
            distance_meters=distance,  # Указываем расстояние
            average_speed=average_speed,  # Сохраняем среднюю скорость
            start_date=datetime.utcnow()
        )
        db.session.add(new_activity)

        # Обновляем прогресс цели, если активность связана с целью
        if new_activity.goal_id:
            goal = Goal.query.get(new_activity.goal_id)
            if not goal:
                abort(404, description="Goal not found")

            goal.last_value += distance  # Увеличиваем прогресс на основании пройденного расстояния
            goal.last_update_date = datetime.utcnow()  # Обновляем дату последнего изменения цели

        db.session.commit()  # Сохраняем активность
        return new_activity

    @staticmethod
    def get_user_activities(user_id):
        # Получаем все активности пользователя
        return Activity.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_activity(user_id, activity_id, data):
        # Обновляем активность
        activity = Activity.query.filter_by(user_id=user_id, id=activity_id).first_or_404()

        if 'activity_type' in data:
            activity.activity_type = data['activity_type']
        if 'duration_seconds' in data:
            activity.duration_seconds = data['duration_seconds']
        if 'distance_meters' in data:
            activity.distance_meters = data['distance_meters']
            activity.average_speed = (
                                           activity.distance_meters / activity.duration_seconds) * 3.6 if activity.duration_seconds > 0 else 0  # Обновляем среднюю скорость

        activity.last_update_date = datetime.utcnow()  # Устанавливаем дату обновления

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Откатываем транзакцию в случае ошибки
            abort(500, description="An error occurred while updating the activity.")

        return activity

    @staticmethod
    def delete_activity(user_id, activity_id):
        # Удаляем активность
        activity = Activity.query.filter_by(user_id=user_id, id=activity_id).first_or_404()
        db.session.delete(activity)
        db.session.commit()


