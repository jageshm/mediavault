from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MediaFile(db.Model):
    """Model for uploaded media files"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    media_type = db.Column(db.String(20), nullable=False)  # 'image' or 'video'
    thumbnail_filename = db.Column(db.String(255), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Add user_id to track who uploaded the file
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def __repr__(self):
        return f"<MediaFile {self.original_filename}>"
    
    def get_file_path(self):
        """Returns the full path to the uploaded file"""
        from app import app
        import os
        return os.path.join(app.config["UPLOAD_FOLDER"], self.filename)
    
    def get_thumbnail_path(self):
        """Returns the full path to the thumbnail"""
        from app import app
        import os
        if not self.thumbnail_filename:
            return None
        return os.path.join(app.config["THUMBNAIL_FOLDER"], self.thumbnail_filename)
    
    def get_file_url(self):
        """Returns the URL for the file"""
        return f"/static/uploads/{self.filename}"
    
    def get_thumbnail_url(self):
        """Returns the URL for the thumbnail"""
        if not self.thumbnail_filename:
            return None
        return f"/static/thumbnails/{self.thumbnail_filename}"
    
    def get_formatted_size(self):
        """Returns the file size in a human-readable format"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024 or unit == 'GB':
                return f"{size:.2f} {unit}"
            size /= 1024

