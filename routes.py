import os
from flask import render_template, request, flash, redirect, url_for, send_from_directory, jsonify, abort
from werkzeug.utils import secure_filename
from app import app, db
from models import MediaFile
from utils import (
    allowed_file, 
    get_file_type, 
    generate_unique_filename, 
    generate_thumbnail, 
    get_default_thumbnail_for_video,
    get_human_readable_size
)
import logging

@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    
    # If user does not select file, browser submits an empty file
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.url)
    
    if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        # Secure the filename and generate a unique name for storage
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
        unique_filename = generate_unique_filename(original_filename)
        
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Determine file type (image or video)
        file_type = get_file_type(file_extension)
        
        # Generate thumbnail for images
        thumbnail_filename = None
        if file_type == 'image':
            thumbnail_filename = f"thumb_{unique_filename}"
            thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], thumbnail_filename)
            if not generate_thumbnail(file_path, thumbnail_path):
                logging.warning(f"Could not generate thumbnail for {unique_filename}")
        
        # Create a new MediaFile record in the database
        new_file = MediaFile(
            filename=unique_filename,
            original_filename=original_filename,
            file_type=file_type,
            file_extension=file_extension,
            file_size=file_size,
            mimetype=file.mimetype,
            thumbnail_filename=thumbnail_filename
        )
        
        db.session.add(new_file)
        db.session.commit()
        
        flash('File successfully uploaded!', 'success')
        return redirect(url_for('gallery'))
    else:
        flash(f'Invalid file type. Allowed types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}', 'danger')
        return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Display all uploaded files in a gallery"""
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of items per page
    
    # Get files from the database with pagination
    files = MediaFile.query.order_by(MediaFile.upload_date.desc()).paginate(page=page, per_page=per_page)
    
    # Add human-readable size to each file
    for file in files.items:
        file.human_readable_size = get_human_readable_size(file.file_size)
    
    return render_template('gallery.html', files=files)

@app.route('/view/<int:file_id>')
def view_file(file_id):
    """View a single file"""
    media_file = MediaFile.query.get_or_404(file_id)
    media_file.human_readable_size = get_human_readable_size(media_file.file_size)
    return render_template('view.html', file=media_file)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads/thumbnails/<filename>')
def thumbnail(filename):
    """Serve thumbnail images"""
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    """Download a file"""
    media_file = MediaFile.query.get_or_404(file_id)
    return send_from_directory(
        app.config['UPLOAD_FOLDER'], 
        media_file.filename, 
        as_attachment=True, 
        download_name=media_file.original_filename
    )

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash(f"The file is too large. Maximum size is {get_human_readable_size(app.config['MAX_CONTENT_LENGTH'])}", 'danger')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500
