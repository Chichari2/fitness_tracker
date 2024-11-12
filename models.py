from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Инициализация SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relations
    activities = db.relationship('Activity', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Activity(db.Model):
  __tablename__ = 'activity'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
  activity_type = db.Column(db.String(50), nullable=False)
  duration_seconds = db.Column(db.Integer, nullable=True)  # Это поле будет заполняться автоматически
  distance_meters = db.Column(db.Float, nullable=True)
  average_speed = db.Column(db.Float, nullable=True)
  start_date = db.Column(db.DateTime, default=datetime.utcnow)
  end_date = db.Column(db.DateTime, nullable=True)
  status = db.Column(db.String(20), default="in progress")

  def to_dict(self):
    activity_dict = {
      'activity_id': self.id,
      'activity_type': self.activity_type,
      'start_date': self.start_date.isoformat(),
      'status': self.status
    }
    if self.duration_seconds is not None:
      activity_dict['duration_seconds'] = self.duration_seconds
    if self.distance_meters is not None:
      activity_dict['distance_meters'] = self.distance_meters
    if self.average_speed is not None:
      activity_dict['average_speed'] = self.average_speed
    if self.end_date is not None:
      activity_dict['end_date'] = self.end_date.isoformat()
    return activity_dict


class Goal(db.Model):
    __tablename__ = 'goal'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    last_value = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    last_update_date = db.Column(db.DateTime)

    # Relations
    activities = db.relationship('Activity', backref='goal', lazy=True)

    def to_dict(self):
        goal_dict = {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'last_value': self.last_value,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
        }
        if self.last_update_date:
            goal_dict['last_update_date'] = self.last_update_date.isoformat()
        return goal_dict

