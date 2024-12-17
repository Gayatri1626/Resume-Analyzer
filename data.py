######################################       RESUME DATA ANALYSIS     ####################################################################

import PyPDF2
import re
import spacy
from spacy.matcher import Matcher
import en_core_web_sm
import json 
from datetime import datetime
from nltk.corpus import wordnet as wn
import nltk
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
import os


##########################################################################################################################################

nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)

#########################################################################################################################################

# A class for analyzing resumes in PDF format.
# Extracts information, identifies sections, and evaluates quality metrics.

class ResumeAnalyzer:
    def __init__(self):
        
        self.nlp = en_core_web_sm.load()
        self.matcher = Matcher(self.nlp.vocab)
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        
        # Define mandatory sections for a complete resume
        self.required_sections = [
            "CONTACT", "SUMMARY", "EXPERIENCE", "EDUCATION", "SKILLS"
        ]
        
        # Define optional sections that enhance resume quality
        self.optional_sections = [
            "PROJECTS", "ACHIEVEMENTS", "CERTIFICATIONS", "LANGUAGES", "INTERESTS"
        ]

        self.custom_action_verbs = [
            'led', 'managed', 'supervised', 'achieved', 'improved', 'created',
            'developed', 'analyzed', 'communicated', 'implemented', 'designed',
            'coordinated', 'launched', 'increased', 'decreased', 'optimized'
        ]
        
        # Define variations of section headers for pattern matching
        self.section_patterns = {
            "CONTACT": ["contact", "contact information", "personal information", "personal details"],
            "SUMMARY": ["summary", "professional summary", "profile", "objective", "about me"],
            "EXPERIENCE": ["experience", "work experience", "professional experience", "employment history", "work history"],
            "EDUCATION": ["education", "educational background", "academic background", "qualifications"],
            "SKILLS": ["skills", "technical skills", "core competencies", "key skills","soft skills"],
            "PROJECTS": ["projects", "academic projects", "personal projects"],
            "ACHIEVEMENTS": ["achievements", "accomplishments", "honors", "awards"],
            "CERTIFICATIONS": ["certifications", "certificates", "professional certifications","courses"],
            "LANGUAGES": ["languages", "language proficiency"],
            "INTERESTS": ["interests", "hobbies", "activities"]
        }

        # Add job-specific skill requirements
        self.job_skills = {
            'data_scientist': [
                'python', 'r', 'sql', 'machine learning', 'deep learning', 
                'statistics', 'data analysis', 'tensorflow', 'pytorch', 
                'scikit-learn', 'pandas', 'numpy'
            ],
            'ai_engineer': [
                'python', 'deep learning', 'neural networks', 'computer vision',
                'nlp', 'machine learning', 'tensorflow', 'pytorch', 'ai models'
            ],
            'software_developer': [
                'python', 'java', 'javascript', 'html', 'css', 'sql',
                'git', 'docker', 'aws', 'rest api', 'nodejs'
            ]
        }
        
        # Create case-insensitive patterns for section matching
        for section, variations in self.section_patterns.items():
            patterns = [[{"LOWER": var.lower()}] for var in variations]
            patterns.extend([[{"LOWER": var.split()[0].lower()}, {"LOWER": var.split()[1].lower()}] 
                           for var in variations if len(var.split()) > 1])
            self.matcher.add(section, patterns)

    
########################################################################################################################################
    # Check if a word is an action verb using WordNet.


    def is_action_verb(self, word):
    
        synsets = wn.synsets(word, pos=wn.VERB)
        if not synsets:
            return False
        
        # Check if any of the verb's senses are categorized as 'verb.action' or 'verb.change'
        for synset in synsets:
            lexname = synset.lexname()
            if lexname.startswith('verb.motion') or lexname.startswith('verb.change') or lexname.startswith('verb.creation'):
                return True
        
        return False

    
    # Extract action verbs from the given text using WordNet.

    def extract_action_verbs(self, text):
        
        words = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        
        action_verbs = set()
        for word, pos in pos_tags:
            if pos.startswith('VB'):  # All verb forms
                if self.is_action_verb(word):
                    action_verbs.add(word.lower())
        
        return action_verbs


##########################################################################################################################################
   
    # Extracts raw text from a PDF file.

    def extract_text_from_pdf(self, pdf_path):
        """
        Extracts raw text from a PDF file.
        Args:
            pdf_path (str): Path to the PDF file
        Returns:
            str: Extracted text content
        """
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    
##########################################################################################################################################

# Cleans and normalizes extracted text.
# Removes special characters and extra whitespace.

    def preprocess_text(self, text):
        
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()
    
##########################################################################################################################################
    
# Saves analysis results to JSON file with timestamp.

    def save_to_json(self, result, output_path):

        result_with_metadata = {
            "timestamp": datetime.now().isoformat(),
            "analysis": result
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_with_metadata, f, indent=2, ensure_ascii=False)



    # Loads analysis results from a JSON file.

    def load_from_json(self, input_path):
        
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)


###########################################################################################################################################

#  Identifies and extracts resume sections using pattern matching.

    def extract_sections(self, text):
        
        doc = self.nlp(text)
        sections = {}
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line_doc = self.nlp(line.strip())
            matches = self.matcher(line_doc)
            
            if matches:
                if current_section:
                    sections[current_section] = '\n'.join(section_content).strip()
                    section_content = []
                current_section = self.nlp.vocab.strings[matches[0][0]]
            elif current_section:
                section_content.append(line.strip())
        
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content).strip()
        
        return sections
    
    #####################################################################################################################################
    
    # Extracts contact information and sections from resume.

    def extract_section_information(self, text):

        sections = self.extract_sections(text)
        
        return {
            'sections': sections
        }


    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from the text using NER and custom rules.
        """
        doc = self.nlp(text)
        skills = set()

        # Extract named entities that might be skills
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG", "GPE"]:
                skills.add(ent.text.lower())

        # Extract potential skills based on POS patterns
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() not in self.stopwords:
                skills.add(token.text.lower())

        return list(skills)
    
    ################################################################################################################################
    # calculate the relevance score for specific job title


    def calculate_skill_match_score(self, resume_text: str, job_title: str) -> tuple:
        if job_title.lower() not in self.job_skills:
            raise ValueError(f"Job title {job_title} not supported")
            
        required_skills = set(self.job_skills[job_title.lower()])
        resume_tokens = set(word.lower() for word in resume_text.split())
        
        matched_skills = required_skills.intersection(resume_tokens)
        skill_score = len(matched_skills) / len(required_skills) * 40
        
        return skill_score, matched_skills
    
    def calculate_experience_score(self, experience_text: str) -> float:
        doc = self.nlp(experience_text.lower())
        
        experience_score = 0
        year_patterns = ['year', 'years', 'yr']
        month_patterns = ['month', 'months']
        
        for token in doc:
            if any(pattern in token.text for pattern in year_patterns):
                experience_score += 10
            elif any(pattern in token.text for pattern in month_patterns):
                experience_score += 5
                
        return min(experience_score, 30)
    
    def calculate_education_score(self, education_text: str) -> float:
        doc = self.nlp(education_text.lower())
        
        education_score = 0
        degree_weights = {
            'phd': 30, 'doctorate': 30,
            'master': 25, 'ms': 25, 'mtech': 25,
            'bachelor': 20, 'btech': 20, 'be': 20
        }
        
        relevant_fields = ['computer', 'data', 'ai', 'artificial intelligence', 
                         'machine learning', 'statistics', 'mathematics']
        
        for token in doc:
            if token.text in degree_weights:
                education_score += degree_weights[token.text]
            if any(field in token.text for field in relevant_fields):
                education_score += 10
                
        return min(education_score, 30)
    
    #################################################################################################################################

    #  Evaluates resume quality metrics.

    def analyze_quality(self, text, extracted_info):
        words = text.split()
        word_count = len(words)
        
        action_verbs = self.extract_action_verbs(text)
        action_verb_count = len(action_verbs)
        
        quantifiable = len(re.findall(r'\d+%|\d+\s*(dollars|usd)', text))
        
        present_sections = set(extracted_info['sections'].keys())
        missing_required = set(self.required_sections) - present_sections
        present_optional = present_sections.intersection(self.optional_sections)
        
        misspelled = len([word for word in set(words) if word not in self.nlp.vocab])
        
        return {
            'word_count': word_count,
            'action_verb_count': action_verb_count,
            'action_verbs_used': list(action_verbs),
            'quantifiable_achievements': quantifiable,
            'present_required_sections': list(present_sections.intersection(self.required_sections)),
            'missing_required_sections': list(missing_required),
            'present_optional_sections': list(present_optional),
            'potential_misspellings': misspelled
        }

    

    
    #   Main method to analyze resume and generate report.
    
    def analyze_resume(self, pdf_path: str, job_title: str = "", json_output_path: str = None, relevance_output_path: str = None) -> Dict[str, Any]:
        # Existing analysis code...
        raw_text = self.extract_text_from_pdf(pdf_path)
        processed_text = self.preprocess_text(raw_text)
        extracted_info = self.extract_section_information(raw_text)
        quality_metrics = self.analyze_quality(processed_text, extracted_info)
        
        # Calculate job relevance scores if job title is provided
        relevance_scores = {}
        if job_title:
            skill_score, matched_skills = self.calculate_skill_match_score(raw_text, job_title)
            experience_score = self.calculate_experience_score(extracted_info['sections'].get('EXPERIENCE', ''))
            education_score = self.calculate_education_score(extracted_info['sections'].get('EDUCATION', ''))
            
            total_score = skill_score + experience_score + education_score
            
            relevance_scores = {
                'overall_score': round(total_score, 2),
                'skill_score': round(skill_score, 2),
                'experience_score': round(experience_score, 2),
                'education_score': round(education_score, 2),
                'matched_skills': list(matched_skills)
            }
        
        result = {
            'extracted_info': extracted_info,
            'quality_metrics': quality_metrics,
            'skills': self.extract_skills(raw_text),
            'job_relevance': relevance_scores,
            'raw_text': raw_text
        }
        
        

        # Save full analysis to a JSON file
        if json_output_path:
            self.save_to_json(result, json_output_path)

        # Save relevance scores to a separate JSON file
        if relevance_output_path:
            self.save_to_json(relevance_scores, relevance_output_path)
        
        return result
    
    def save_to_json(self, data: Dict[str, Any], json_file_path: str):
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)


    
    #####################################################################################################################################


if __name__ == "__main__":
    analyzer = ResumeAnalyzer()
    
    # Define paths
    pdf_path = r"C:\Users\aryan\Downloads\Sofware-Tester-NaveenDudhyal (4).pdf"
    job_title = "software_developer"
    output_file = r"C:\Users\Projects\Dataextract\resume_analysis.json"
    relevance_output_file = r"C:\Users\Projects\Dataextract\job_relevance.json"

    try:
        # Analyze resume and save results
        result = analyzer.analyze_resume(pdf_path, job_title=job_title, json_output_path=output_file, relevance_output_path=relevance_output_file)
        print(f"Full analysis saved to {output_file}")
        print(f"Relevance scores saved to {relevance_output_file}")

        # Optionally, load and print the results
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                loaded_result = json.load(f)
                print("\nLoaded analysis:", json.dumps(loaded_result, indent=2))

        if os.path.exists(relevance_output_file):
            with open(relevance_output_file, 'r') as f:
                loaded_relevance_scores = json.load(f)
                print("\nLoaded relevance scores:", json.dumps(loaded_relevance_scores, indent=2))

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")