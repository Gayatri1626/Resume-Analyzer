Here's a `README.md` file for your **Resume Data Analysis** project:

---

# 📄 Resume Data Analysis

## 🚀 **Project Overview**
The **Resume Data Analysis** project extracts, analyzes, and evaluates resumes in PDF format. It identifies sections, extracts contact information, extracts skills, and calculates quality scores based on experience, education, and skills match with specific job roles. The analysis results are saved to JSON format for easy storage and retrieval.

---

## 📚 **Features**

✅ Extracts text from PDF resumes  
✅ Identifies and extracts key sections: `Contact`, `Summary`, `Experience`, `Education`, `Skills`, etc.  
✅ Extracts action verbs using **WordNet** and **NLTK**  
✅ Calculates quality scores:
- **Skill match score:** Matches resume skills with job-specific skills  
- **Experience score:** Analyzes years and months of experience  
- **Education score:** Evaluates the degree and relevant fields  
✅ Saves analysis results to a JSON file with a timestamp  
✅ Supports multiple job profiles: `Data Scientist`, `AI Engineer`, `Software Developer`  

---

## 🛠️ **Tech Stack**

- **Python Libraries:**  
  - `PyPDF2` → PDF extraction  
  - `spaCy` → NLP processing  
  - `NLTK` → Natural language processing (WordNet and POS tagging)  
  - `sklearn` → TF-IDF vectorizer for text analysis  
  - `datetime` → Timestamp for saving analysis results  
- **File Format:**  
  - PDF input files  
  - JSON output files  

---

## 🔥 **Installation**

1. **Clone the Repository**
```bash
git clone <repository_url>
cd resume-data-analysis
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK Resources**
```python
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
```

---

## 📊 **Usage**

1. **Run the Script**
```bash
python resume_analyzer.py
```

2. **Input PDF Resume**
- Place the PDF file in the working directory
- Update the PDF file path in the script:
```python
pdf_path = "path/to/resume.pdf"
```

3. **Output**
- The extracted sections, skills, and scores will be saved as a JSON file:
```json
{
  "timestamp": "2025-03-19T12:45:32",
  "analysis": {
    "sections": {
      "CONTACT": "John Doe\njohn.doe@email.com\n+1-234-567-890",
      "EXPERIENCE": "...",
      "SKILLS": "Python, SQL, Data Analysis"
    },
    "skill_match_score": 35.0,
    "experience_score": 25.0,
    "education_score": 30.0
  }
}
```

---

## ✅ **Scoring Criteria**

- **Skill Match Score:**  
  - Compares extracted skills with job-specific skills  
  - Max score: **40 points**

- **Experience Score:**  
  - Based on experience duration (years and months)  
  - Max score: **30 points**

- **Education Score:**  
  - Degree level and relevant fields  
  - Max score: **30 points**

---

## 🛠️ **Customization**

- **Add new job profiles**
  - Edit the `self.job_skills` dictionary in the `ResumeAnalyzer` class:
```python
self.job_skills = {
    'data_scientist': ['python', 'sql', 'machine learning'],
    'ai_engineer': ['tensorflow', 'pytorch', 'nlp'],
    'software_developer': ['java', 'aws', 'docker']
}
```

- **Update Section Patterns**
  - Modify `self.section_patterns` to add or customize section names.

---

## ⚙️ **Directory Structure**
```
/resume-data-analysis  
 ├── resume_analyzer.py        # Main script  
 ├── requirements.txt          # Dependencies  
 ├── sample_resume.pdf         # Sample PDF resume  
 ├── output.json               # Analysis result in JSON  
 ├── README.md                 # Documentation  
```

---

## 📌 **To-Do List**

- [ ] Improve NLP accuracy for section extraction  
- [ ] Add support for more job profiles  
- [ ] Integrate visualizations (matplotlib) for resume scoring  
- [ ] Add functionality to compare multiple resumes  

---

## 📝 **License**
This project is licensed under the MIT License.  

---

## ✨ **Contributors**
- [Gayatri Ghorpade](https://github.com/your-github-profile)  

---

✅ **Feel free to contribute and improve this project!**
