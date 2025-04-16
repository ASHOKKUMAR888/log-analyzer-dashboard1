from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Set up the directory where files will be uploaded
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'xyz'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for uploading log files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'logFile' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['logFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        # Save the file to the uploads folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Parse and analyze the file
        analysis = analyze_log(filepath)
        return jsonify(analysis), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

# Function to analyze the log file
def analyze_log(file_path):
    with open(file_path, 'r') as f:
        logs = f.readlines()

    analysis = {
        "total_logs": len(logs),
        "errors": 0,
        "warnings": 0,
        "info": 0
    }

    for log in logs:
        if "error" in log.lower():
            analysis["errors"] += 1
        elif "warning" in log.lower():
            analysis["warnings"] += 1
        elif "info" in log.lower():
            analysis["info"] += 1

    return analysis

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
