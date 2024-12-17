import os
import json
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from data import ResumeAnalyzer
from flask_cors import CORS


# Determine the base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))
CORS(app)  # This will enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize resume analyzer
analyzer = ResumeAnalyzer()

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Handle resume analysis request.
    Expects a PDF file and a job title via multipart/form-data.
    Returns JSON with analysis results.
    """
    # Check if the post request has the file part
    if 'resumeFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['resumeFile']
    job_title = request.form.get('jobTitle')

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check file type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

    # Save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Perform resume analysis
        result = analyzer.analyze_resume(
            filepath, 
            job_title=job_title, 
            json_output_path=os.path.join(app.config['UPLOAD_FOLDER'], 'resume_analysis.json'),
            relevance_output_path=os.path.join(app.config['UPLOAD_FOLDER'], 'job_relevance.json')
        )

        # Remove the uploaded file after processing
        os.remove(filepath)

        return jsonify(result)

    except Exception as e:
        # Log the error for server-side debugging
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': 'Failed to analyze resume', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)