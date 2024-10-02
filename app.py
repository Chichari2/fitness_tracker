from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db  # Import db from models
from api import api_bp as api_blueprint


# Инициализация приложения и конфигурация
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация баз данных и миграций
db.init_app(app)  # Инициализируем db с приложением
migrate = Migrate(app, db)

# Инициализация JWT
jwt = JWTManager(app)

# Register of API Blueprint

app.register_blueprint(api_blueprint, url_prefix='/api')


# main page
@app.route('/')
def home():
    return "Welcome to the Fitness Tracker API!"


if __name__ == "__main__":
    app.run(debug=True)
