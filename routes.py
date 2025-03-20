import os
import uuid
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

from app import app, db
from models import MediaFile
from utils import generate_thumbnail, allowed_file, get_media_type

# Add current date to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    
    # If user does not select file, browser submits an empty part
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Create a secure filename with unique id to prevent collisions
        original_filename = file.filename
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        
        # Determine media type
        media_type = get_media_type(original_filename)
        
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Generate thumbnail if it's an image
        thumbnail_filename = None
        if media_type == 'image':
            thumbnail_filename = f"thumb_{unique_filename}"
            thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], thumbnail_filename)
            if not generate_thumbnail(file_path, thumbnail_path):
                thumbnail_filename = None
        
        # Create database entry
        media_file = MediaFile(
            filename=unique_filename,
            original_filename=original_filename,
            mime_type=file.content_type,
            file_size=file_size,
            media_type=media_type,
            thumbnail_filename=thumbnail_filename
        )
        
        db.session.add(media_file)
        db.session.commit()
        
        # If this is an AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'redirect': url_for('gallery')
            })
        
        flash('File successfully uploaded', 'success')
        return redirect(url_for('gallery'))
    else:
        flash('File type not allowed', 'danger')
        return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Display gallery of uploaded files"""
    media_files = MediaFile.query.order_by(MediaFile.upload_date.desc()).all()
    return render_template('gallery.html', media_files=media_files)

@app.route('/view/<int:file_id>')
def view_file(file_id):
    """View a specific file"""
    media_file = MediaFile.query.get_or_404(file_id)
    return render_template('view.html', media_file=media_file)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    """Download a specific file"""
    media_file = MediaFile.query.get_or_404(file_id)
    uploads_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
    return send_from_directory(
        directory=uploads_dir, 
        path=media_file.filename,
        as_attachment=True,
        download_name=media_file.original_filename
    )

@app.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    """Delete a specific file"""
    media_file = MediaFile.query.get_or_404(file_id)
    
    # Delete the actual file
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], media_file.filename))
        
        # Delete thumbnail if it exists
        if media_file.thumbnail_filename:
            thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], media_file.thumbnail_filename)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
    except Exception as e:
        app.logger.error(f"Error deleting file: {e}")
    
    # Delete database record
    db.session.delete(media_file)
    db.session.commit()
    
    flash('File successfully deleted', 'success')
    return redirect(url_for('gallery'))

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    flash('File too large', 'danger')
    return redirect(url_for('index')), 413

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404
