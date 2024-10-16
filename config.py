import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Замените на URI вашей базы данных PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')  # Вы можете установить секретный ключ через переменные окружения


