from datetime import datetime
from models import Activity, db
from flask import abort

class ActivityManager:

    @staticmethod
    def create_activity(user_id, data):
        activity_type = data['activity_type']  # only activity_type is required

        new_activity = Activity(
            user_id=user_id,
            activity_type=activity_type,
            start_date=datetime.utcnow(),
            status="in progress"  # activity starts with "in progress" status
        )
        db.session.add(new_activity)
        db.session.commit()
        return new_activity

    @staticmethod
    def get_user_activities(user_id):
        return Activity.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update_activity(user_id, activity_id, data):
        activity = Activity.query.filter_by(user_id=user_id, id=activity_id).first_or_404()
        if 'activity_type' in data:
            activity.activity_type = data['activity_type']
        if 'duration_seconds' in data:
            activity.duration_seconds = data['duration_seconds']
        if 'distance_meters' in data:
            activity.distance_meters = data['distance_meters']
            activity.average_speed = (activity.distance_meters / activity.duration_seconds) * 3.6 if activity.duration_seconds > 0 else 0

        activity.last_update_date = datetime.utcnow()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description="An error occurred while updating the activity.")
        return activity

    @staticmethod
    def delete_activity(user_id, activity_id):
        activity = Activity.query.filter_by(user_id=user_id, id=activity_id).first_or_404()
        db.session.delete(activity)
        db.session.commit()

    @staticmethod
    def finish_activity(user_id, activity_id, distance_meters):
        activity = Activity.query.filter_by(user_id=user_id, id=activity_id).first_or_404()

        # Если активность уже завершена, возвращаем ошибку
        if activity.status == "finished":
            abort(400, description="Activity is already finished")

        # Устанавливаем статус как "finished" и записываем дату окончания
        activity.status = "finished"
        activity.end_date = datetime.utcnow()

        # Расчитываем продолжительность активности
        activity.duration_seconds = int((activity.end_date - activity.start_date).total_seconds())

        # Устанавливаем расстояние, если оно передано
        activity.distance_meters = distance_meters

        # Расчитываем среднюю скорость
        activity.average_speed = (
                                       activity.distance_meters / activity.duration_seconds) * 3.6 if activity.duration_seconds > 0 else 0

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description="An error occurred while finishing the activity.")

        return activity