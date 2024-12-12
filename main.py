import os
import logging
from flask import Flask
from flask_cors import CORS
from app.routes import initialize_routes
from utils.vertexAIclient import start_vertex


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Ensure the uploads directory exists
    uploads_path = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(uploads_path):
        os.makedirs(uploads_path)

    initialize_routes(app)
    return app

def initialize_logger(app):
    """Setup logging for debugging purposes."""
    logger = logging.getLogger('flask.app')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    app.logger = logger

if __name__ == "__main__":
    app = create_app()
    start_vertex(app)
    initialize_logger(app)
    app.run(debug=True)
