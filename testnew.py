from flask import Flask, request
from utils.vertexAIclient import process_resume_and_analyze, start_vertex

app = Flask(__name__)

# Initialize Vertex AI client
start_vertex(app)

@app.route('/upload', methods=['POST'])
def upload_resume():
    return process_resume_and_analyze()

if __name__ == '__main__':
    app.run(debug=True)
