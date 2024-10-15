from models import User, db
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError
# Импортируем email-validator


class UserManager:

    @staticmethod
    def create_user(data):
        if not data or 'username' not in data or 'password' not in data or 'email' not in data:
            raise ValueError("Missing required fields")

        # Валидация email
        try:
            valid_email = validate_email(data['email'])
            email = valid_email.email  # Получаем нормализованный email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {str(e)}")

        # Проверка на существование пользователя с таким же именем
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            raise ValueError("Username already taken")

        # Проверка на существование пользователя с таким же email
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            raise ValueError("Email already registered")

        new_user = User(username=data['username'], email=email)
        new_user.set_password(data['password'])

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            raise Exception("An error occurred during registration")

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user is None or not user.verify_password(password):
            raise ValueError("Bad username or password")

        return user
