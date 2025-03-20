from datetime import datetime
from app import db

class MediaFile(db.Model):
    """Model for storing information about uploaded media files"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # 'image' or 'video'
    file_extension = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    mimetype = db.Column(db.String(100), nullable=False)
    thumbnail_filename = db.Column(db.String(255), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MediaFile {self.filename}>'
    
    def to_dict(self):
        """Convert the model to a dictionary for easy serialization"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_extension': self.file_extension,
            'file_size': self.file_size,
            'mimetype': self.mimetype,
            'thumbnail_filename': self.thumbnail_filename,
            'upload_date': self.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        }
