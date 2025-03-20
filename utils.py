import os
import uuid
from PIL import Image, UnidentifiedImageError
import logging

def allowed_file(filename, allowed_extensions):
    """Check if the file extension is in the allowed extensions list"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_type(extension):
    """Determine if the file is an image or video based on its extension"""
    image_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    video_extensions = {'mp4', 'mov', 'avi', 'webm'}
    
    if extension in image_extensions:
        return 'image'
    elif extension in video_extensions:
        return 'video'
    return 'unknown'

def generate_unique_filename(original_filename):
    """Generate a unique filename for storage to prevent overwriting"""
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_id = uuid.uuid4().hex
    return f"{unique_id}.{extension}"

def generate_thumbnail(file_path, thumbnail_path, max_size=(200, 200)):
    """Generate a thumbnail for an image file"""
    try:
        with Image.open(file_path) as img:
            img.thumbnail(max_size)
            img.save(thumbnail_path)
            return True
    except (UnidentifiedImageError, IOError, FileNotFoundError) as e:
        logging.error(f"Error generating thumbnail: {e}")
        return False

def get_default_thumbnail_for_video():
    """Return the path to a default thumbnail for video files"""
    # We'll use a font awesome icon in the template instead
    return None

def get_human_readable_size(size_in_bytes):
    """Convert file size from bytes to a human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"
