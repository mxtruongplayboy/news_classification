import pandas as pd
import re
import py_vncorenlp
import os

class TextCleaner:
    def __init__(self, stopwords_file, abbreviations_file, vncorenlp_model_dir):
        # Load stopwords and abbreviations
        self.stopwords = self.load_stopwords(stopwords_file)
        self.abbreviations = self.load_abbreviations(abbreviations_file)
        
        # Load VnCoreNLP model
        self.model = py_vncorenlp.VnCoreNLP(save_dir=vncorenlp_model_dir)
    
    def load_stopwords(self, file_path):
        """Load stopwords from a file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    
    def load_abbreviations(self, file_path):
        """Load abbreviations from a file"""
        abbreviations = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    abbreviations[parts[0].strip()] = parts[1].strip()
        return abbreviations
    
    def replace_abbreviations(self, text):
        """Replace abbreviations with full text"""
        for abbr, full_text in self.abbreviations.items():
            text = re.sub(rf'\b{abbr}\b', full_text, text, flags=re.IGNORECASE)
        return text
    
    def clean_text(self, text):
        """Remove punctuation and special characters"""
        return re.sub(r'[^\w\s]', '', text)
    
    def tokenize_text(self, text):
        """Tokenize text using VnCoreNLP"""
        return self.model.annotate_text(text)
    
    def extract_wordforms(self, tokens_dict):
        """Extract word forms from tokenized text"""
        tokens = tokens_dict.get(0, [])
        return [token['wordForm'].lower() for token in tokens if isinstance(token, dict) and token.get('wordForm')]
    
    def remove_stopwords(self, wordforms):
        """Remove stopwords from a list of wordforms"""
        return [word for word in wordforms if word not in self.stopwords]
    
    def remove_numbers(self, wordforms):
        """Remove words containing numbers"""
        return [word for word in wordforms if not re.search(r'\d', word)]
    
    def join_to_sentence(self, wordforms):
        """Join wordforms back into a sentence"""
        return ' '.join(wordforms)
    
    def process_text(self, title, description, content):
        """Process the input text and return cleaned version"""
        # Replace abbreviations
        title = self.replace_abbreviations(title)
        description = self.replace_abbreviations(description)
        content = self.replace_abbreviations(content)
        
        # Clean the text
        title = self.clean_text(title)
        description = self.clean_text(description)
        content = self.clean_text(content)
        
        # Tokenize the text
        title_tokens = self.tokenize_text(title)
        description_tokens = self.tokenize_text(description)
        content_tokens = self.tokenize_text(content)
        
        # Extract wordforms and remove stopwords and numbers
        title_cleaned = self.extract_wordforms(title_tokens)
        description_cleaned = self.extract_wordforms(description_tokens)
        content_cleaned = self.extract_wordforms(content_tokens)
        
        title_cleaned = self.remove_stopwords(title_cleaned)
        description_cleaned = self.remove_stopwords(description_cleaned)
        content_cleaned = self.remove_stopwords(content_cleaned)
        
        title_cleaned = self.remove_numbers(title_cleaned)
        description_cleaned = self.remove_numbers(description_cleaned)
        content_cleaned = self.remove_numbers(content_cleaned)
        
        # Join cleaned text back into sentences
        title_cleaned = self.join_to_sentence(title_cleaned)
        description_cleaned = self.join_to_sentence(description_cleaned)
        content_cleaned = self.join_to_sentence(content_cleaned)
        
        return title_cleaned, description_cleaned, content_cleaned
