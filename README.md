# Resume Analyzer 📄🔍

## Project Overview

The Resume Analyzer is an intelligent web application that performs comprehensive analysis of PDF resumes, providing insights into resume quality, job relevance, and skill matching.

## Features

### 1. Resume Analysis Capabilities
- Extract key sections from resume
- Analyze resume quality metrics
- Calculate job-specific relevance scores
- Identify skills and action verbs
- Support for multiple job titles

### 2. Job Title Support
Currently supports analysis for:
- Data Scientist
- AI Engineer
- Software Developer

## Tech Stack

- **Backend**: Python
  - PyPDF2 for PDF text extraction
  - SpaCy for natural language processing
  - NLTK for linguistic processing
  - Scikit-learn for text analysis

- **Web Framework**: Flask
- **Frontend**: HTML, Bootstrap, JavaScript
- **Data Processing**: Pandas, NumPy

## Prerequisites

### Python Dependencies
- PyPDF2
- spacy
- en_core_web_sm
- nltk
- flask
- flask-cors
- scikit-learn

### Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

4. Download NLTK resources
```python
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
```

## Running the Application

```bash
python app.py
```

Navigate to `http://localhost:5000` in your web browser.

## How It Works

### Resume Analysis Process
1. PDF text extraction
2. Text preprocessing
3. Section identification
4. Skill matching
5. Quality metric calculation
6. Job relevance scoring

### Scoring Mechanism
- **Skill Match**: 40 points
- **Experience**: Up to 30 points
- **Education**: Up to 30 points
- **Total Possible Score**: 100 points

## Configuration

- Modify `job_skills` in `data.py` to add or update job-specific skills
- Customize scoring weights in scoring methods

## Security Features
- File type validation
- Maximum file size limit
- Secure file handling
- Temporary file deletion

## Limitations
- Works best with well-structured, text-based PDFs
- Job title must be predefined
- Limited to English language resumes

## Future Enhancements
- Add more job titles
- Improve NLP accuracy
- Implement advanced skill recognition
- Create more detailed scoring mechanisms

## Troubleshooting
- Ensure all dependencies are installed
- Check PDF formatting
- Verify file permissions

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## Contact
gayatrighorpade409@gmail.com
9623520301
