from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi Database & Migrasi
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes di baris paling bawah
from app import routes