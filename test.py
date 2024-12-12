from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/generatemockquestions', methods=['POST'])
def generate_mock_questions():
    # Check if the form data has the job description
    job_description = request.form.get('jobDescription')
    if not job_description:
        return jsonify({"message": "Job description is required"}), 400
    
    # Check if a file is attached
    file = request.files.get('file')
    if file:
        # Process the file (for example, print the filename)
        print(f"File received: {file.filename}")
    else:
        print("No file received")
    
    # Respond with the data that was received (for debugging purposes)
    return jsonify({
        "message": "Successfully received job description and file (if any)",
        "jobDescription": job_description,
        "file": file.filename if file else None
    })

if __name__ == '__main__':
    app.run(debug=True,port=5000)
