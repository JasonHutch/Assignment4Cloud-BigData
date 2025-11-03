import os
from typing import Dict, List

from helper import Helper
from transformations import Transformations
from collections import namedtuple

DocumentPosition = namedtuple('DocumentPosition', ['doc_id', 'paragraph_num', 'word_position'])

class SearchIndex:
    def __init__(self):
        self.index = dict()
        self.transformations = Transformations()
        self.helper = Helper()
        self.STOP_WORDS = {
            "a","an","the","and","or","but","if","while","is","are","was","were",
            "in","on","at","by","for","with","about","of","to","from","as","it",
            "i","you","he","she","they","we","me","my","your","his","her",
            "myself", "our", "ours", "ourselves", "yourself", "yourselves", 
            "him", "his", "himself", "her", "hers", "herself", "it", "its", 
            "itself", "them", "their", "theirs", "themselves", "what", "which", 
            "who", "whom", "this", "that", "these", "those", "am", "is", "are", 
            "was", "were", "be", "been", "being", "have", "has", "had", "having", 
            "do", "does", "did", "doing", "would", "should", "could", "ought", 
            "i'm", "you're", "he's", "she's", "it's", "we're", "they're", 
            "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd", 
            "she'd", "we'd", "they'd", "i'll", "you'll", "he'll", "she'll", 
            "we'll", "they'll", "isn't", "aren't", "wasn't", "weren't", 
            "hasn't", "haven't", "hadn't", "doesn't", "don't", "didn't", 
            "won't", "wouldn't", "shan't", "shouldn't", "can't", "cannot", 
            "couldn't", "mustn't", "let's", "that's", "who's", "what's", 
            "here's", "there's", "when's", "where's", "why's", "how's", 
            "because", "against", "between", "into", "through", "during", 
            "before", "after", "above", "below", "up", "down", "out", 
            "on", "off", "over", "under", "again", "further", "then", 
            "once", "here", "there", "when", "where", "why", "how", 
            "all", "any", "both", "each", "few", "more", "most", 
            "other", "some", "such", "no", "nor", "not", "only", 
            "own", "same"
        }
    
    def index_text_documents(self,path:str) -> None:
        """
        iterates through text documents at a certain path. Processing them and adding them to the search index
        """
        
        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                with open(os.path.join(path, filename), 'r') as file:
                    content = file.read()
                    paragraphs = content.split('\n\n')
                    
                    for i, para in enumerate(paragraphs):
                        tokens = self.process_text(para)
                        self.index_tokens(tokens, i, filename)
                        
            
    def process_text(self, input_text:str) -> List[str]:
        input_text = input_text.lower()
        input_text = ''.join(c for c in input_text if ord(c) < 127)
        input_text = self.transformations.remove_puncuation(input_text)
        tokens = self.transformations.remove_stop_words(input_text)
        
        return tokens
    
    def index_tokens(self,tokens:List[str], paragraph_number:int, document_id:str):
        for position, token in enumerate(tokens):
            metadata = DocumentPosition(
                doc_id=document_id,
                paragraph_num=paragraph_number,
                word_position=position
            )
            
            if token in self.index:
                self.index[token].append(metadata)
            else:
                self.index[token] = [metadata]
                
    def search(self, query: str) -> Dict[str, List[DocumentPosition]]:
        """
        Search for a term and return matching documents with positions
        """
        tokens = self.process_text(query)
        results = {}
        
        for token in tokens:
            if token in self.index:
                results[token] = self.index[token]
        
        return results

    def search_phrase(self, phrase: str) -> List[DocumentPosition]:
        """
        Search for exact phrase matches using word positions
        """
        tokens = self.process_text(phrase)
        
        if not tokens:
            return []
        
        # Get all positions of first token
        if tokens[0] not in self.index:
            return []
        
        results = []
        
        for first_pos in self.index[tokens[0]]:
            # Check if remaining tokens appear consecutively
            match = True
            for i, token in enumerate(tokens[1:], start=1):
                if token not in self.index:
                    match = False
                    break
                
                # Look for same doc/para with word_position = first_pos.word_position + i
                expected_pos = DocumentPosition(
                    doc_id=first_pos.doc_id,
                    paragraph_num=first_pos.paragraph_num,
                    word_position=first_pos.word_position + i
                )
                
                if expected_pos not in self.index[token]:
                    match = False
                    break
            
            if match:
                results.append(first_pos)
        
        return results






