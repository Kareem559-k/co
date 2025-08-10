from flask import Blueprint, send_from_directory, current_app
import os

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def serve_index():
    """Serve the main React application"""
    return send_from_directory(current_app.static_folder, 'index.html')

@frontend_bp.route('/<path:path>')
def serve_static(path):
    """Serve static files or fallback to index.html for React routing"""
    static_file_path = os.path.join(current_app.static_folder, path)
    
    # If the file exists, serve it
    if os.path.exists(static_file_path):
        return send_from_directory(current_app.static_folder, path)
    
    # Otherwise, serve index.html for React routing
    return send_from_directory(current_app.static_folder, 'index.html')

