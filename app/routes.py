# routes.py
from flask import Blueprint
from app.controllers.test import test_prompt
from app.controllers.generateMockQuestions import generate_mock_questions

def initialize_routes(app):
    # Create a Blueprint for API routes
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # Define GET route for /api/test
    api_bp.add_url_rule('/test', view_func=test_prompt, methods=['GET'])
    
    # Define POST route for /api/generatemockquestions
    api_bp.add_url_rule('/generatemockquestions', view_func=generate_mock_questions, methods=['POST'])

    # Register the Blueprint with the Flask app
    app.register_blueprint(api_bp)
