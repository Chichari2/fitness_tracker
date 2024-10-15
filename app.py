from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db  # Import db from models
from api import api_bp as api_blueprint
from werkzeug.exceptions import BadRequest, Unauthorized

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

# Обработчик для 400 ошибок (Bad Request)
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    response = jsonify({'message': str(e)})
    response.status_code = 400
    return response

# Обработчик для 401 ошибок (Unauthorized)
@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    response = jsonify({'message': str(e)})
    response.status_code = 401
    return response

if __name__ == "__main__":
    app.run(debug=True)

