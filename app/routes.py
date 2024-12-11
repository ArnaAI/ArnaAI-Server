from flask import Blueprint
from python_server.app.controllers.test import test_prompt

def initialize_routes(app):
    # Create a Blueprint for API routes
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # Define GET route for /api/zenai

    # Define POST route for /api/zenai
    api_bp.add_url_rule('/test', view_func=test_prompt, methods=['GET'])

    # Register the Blueprint with the Flask app
    app.register_blueprint(api_bp)
