import os
import uuid
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user

from app import app, db
from models import MediaFile, User
from utils import generate_thumbnail, allowed_file, get_media_type
from forms import LoginForm, RegistrationForm, UploadForm

# Add current date to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    """Main page with upload form"""
    form = UploadForm()
    return render_template('index.html', form=form)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file uploads (authenticated users only)"""
    form = UploadForm()
    
    if not form.validate_on_submit():
        flash('No file selected or invalid file', 'danger')
        return redirect(url_for('index'))
        
    file = form.file.data
    
    if not allowed_file(file.filename):
        flash('File type not allowed', 'danger')
        return redirect(url_for('index'))
    
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
    
    # Create database entry with the current user's ID
    media_file = MediaFile(
        filename=unique_filename,
        original_filename=original_filename,
        mime_type=file.content_type,
        file_size=file_size,
        media_type=media_type,
        thumbnail_filename=thumbnail_filename,
        user_id=current_user.id
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
@login_required
def delete_file(file_id):
    """Delete a specific file (authenticated users only)"""
    media_file = MediaFile.query.get_or_404(file_id)
    
    # Check if the current user is the owner of the file
    if media_file.user_id != current_user.id:
        flash('You do not have permission to delete this file', 'danger')
        return redirect(url_for('gallery'))
    
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

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_for('index') not in next_page:
            next_page = url_for('index')
        
        flash('Login successful!', 'success')
        return redirect(next_page)
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
