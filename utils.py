import os
from PIL import Image, UnidentifiedImageError
from app import app

def allowed_file(filename):
    """Check if the file extension is allowed"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    # Check if extension is in any of the allowed categories
    for media_type, extensions in app.config['ALLOWED_EXTENSIONS'].items():
        if extension in extensions:
            return True
    
    return False

def get_media_type(filename):
    """Determine the media type based on file extension"""
    if '.' not in filename:
        return None
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    for media_type, extensions in app.config['ALLOWED_EXTENSIONS'].items():
        if extension in extensions:
            return media_type
    
    return None

def generate_thumbnail(source_path, destination_path, size=(200, 200)):
    """Generate a thumbnail for an image file
    
    Args:
        source_path: Path to the source image
        destination_path: Path where the thumbnail should be saved
        size: Thumbnail dimensions as a tuple (width, height)
        
    Returns:
        Boolean indicating success or failure
    """
    try:
        # Open the image
        with Image.open(source_path) as img:
            # Convert to RGB if necessary (e.g., for PNGs with transparency)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Need to convert to RGBA first to preserve alpha during resize, then to RGB
                img = img.convert('RGBA')
                background = Image.new('RGBA', img.size, (255, 255, 255))
                img = Image.alpha_composite(background, img).convert('RGB')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create a thumbnail
            img.thumbnail(size, Image.LANCZOS)
            
            # Save the thumbnail
            img.save(destination_path, format='JPEG', quality=85)
            
            return True
    except (IOError, OSError, UnidentifiedImageError) as e:
        app.logger.error(f"Error generating thumbnail: {e}")
        return False
    except Exception as e:
        app.logger.error(f"Unexpected error generating thumbnail: {e}")
        return False
