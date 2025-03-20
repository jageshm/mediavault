import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to upload media files.'
login_manager.login_message_category = 'info'

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure the database - always use PostgreSQL if DATABASE_URL is available
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure upload settings
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["THUMBNAIL_FOLDER"] = "static/thumbnails"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max upload size
app.config["ALLOWED_EXTENSIONS"] = {
    "image": {"png", "jpg", "jpeg", "gif"},
    "video": {"mp4", "webm", "ogg"}
}

# Initialize the app with SQLAlchemy and LoginManager
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Create upload directories if they don't exist
with app.app_context():
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["THUMBNAIL_FOLDER"], exist_ok=True)
    
    # Import models and create tables
    import models
    db.create_all()
    
    # Import and register routes
    from routes import *

