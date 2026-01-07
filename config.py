import os

class Config:
    # Setting Database
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASS = ''
    DB_NAME = 'smartlamp_db'
    
    # Koneksi untuk SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Setting Upload & Security
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'app/static/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}