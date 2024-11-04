from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Инициализация SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
  __tablename__ = 'user'  # Явное указание имени таблицы

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), nullable=False, unique=True)
  email = db.Column(db.String(100), nullable=False, unique=True)
  password_hash = db.Column(db.String(255), nullable=False)

  # Отношения с другими моделями
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
  __tablename__ = 'activity'  # Явное указание имени таблицы

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)  # Внешний ключ для связи с целью
  activity_type = db.Column(db.String(50), nullable=False)
  duration_seconds = db.Column(db.Integer, nullable=False)
  distance_meters = db.Column(db.Float, nullable=False)  # Добавляем поле для расстояния
  average_speed = db.Column(db.Float, nullable=False)  # Поле для средней скорости
  start_date = db.Column(db.DateTime, default=datetime.utcnow)
  last_update_date = db.Column(db.DateTime)

  def to_dict(self):
    activity_dict = {
      'id': self.id,
      'activity_type': self.activity_type,
      'duration_seconds': self.duration_seconds,
      'distance_meters': self.distance_meters,  # Добавляем расстояние
      'average_speed': self.average_speed,  # Добавляем среднюю скорость
      'start_date': self.start_date.isoformat()
    }
    if self.last_update_date is not None:
      activity_dict['last_update_date'] = self.last_update_date.isoformat()
    return activity_dict


class Goal(db.Model):
  __tablename__ = 'goal'  # Явное указание имени таблицы

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  value = db.Column(db.Integer, nullable=False)
  last_value = db.Column(db.Integer, default=0)  # Прогресс выполнения цели
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=False)
  last_update_date = db.Column(db.DateTime)  # Добавляем поле для последнего обновления

  # Связь с активностями
  activities = db.relationship('Activity', backref='goal', lazy=True)

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'value': self.value,
      'last_value': self.last_value,
      'start_date': self.start_date.isoformat(),
      'end_date': self.end_date.isoformat(),
      'last_update_date': self.last_update_date.isoformat() if self.last_update_date else None
    }
