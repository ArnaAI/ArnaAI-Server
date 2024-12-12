from flask import Blueprint
from utils.vertexAIclient import process_resume_and_analyze

def initialize_routes(app):
    """Setup routes for the Flask application."""
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # Define POST route for file upload
    api_bp.add_url_rule('/upload', view_func=process_resume_and_analyze, methods=['POST'])

    # Register the Blueprint with the Flask app
    app.register_blueprint(api_bp)
