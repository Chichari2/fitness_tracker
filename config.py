class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/site.db'  # или другой URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key' 
