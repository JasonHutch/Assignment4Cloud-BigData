import os
from typing import Dict, List, Tuple
from collections import Counter

from helper import Helper
from lib.transformations import Transformations
from lib.language_detector import LanguageDetector
from collections import namedtuple

DocumentPosition = namedtuple('DocumentPosition', ['doc_id', 'paragraph_num', 'word_position', 'language'])

class SearchIndex:
    def __init__(self):
        self.index = dict()
        self.transformations = Transformations()
        self.language = LanguageDetector()
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
    
    def index_text_documents(self,path:str, language:str = 'en') -> None:
        """
        iterates through text documents at a certain path. Processing them and adding them to the search index
        """

        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                with open(os.path.join(path, filename), 'r') as file:
                    content = file.read()
                    
                    # Detect language from entirety of content
                    input_distribution = self.language.get_distribution_from_text(content)
                    language = self.language.detect_language(input_distribution)
                    
                    paragraphs = content.split('\n\n')
                    for i, para in enumerate(paragraphs):
                        tokens = self.process_text(para, language)
                        self.index_tokens(tokens, i, filename, language)
                        
            
    def process_text(self, input_text:str, language:str = 'en') -> List[str]:
        input_text = input_text.lower()
        # For French, preserve accented characters; for English, remove non-ASCII
        if language != 'fr':
            input_text = ''.join(c for c in input_text if ord(c) < 127)
        input_text = self.transformations.remove_puncuation(input_text)
        tokens = self.transformations.remove_stop_words(input_text, language)

        return tokens
    
    def index_tokens(self,tokens:List[str], paragraph_number:int, document_id:str, language:str = 'en'):
        for position, token in enumerate(tokens):
            metadata = DocumentPosition(
                doc_id=document_id,
                paragraph_num=paragraph_number,
                word_position=position,
                language=language
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
                    word_position=first_pos.word_position + i,
                    language=first_pos.language
                )
                
                if expected_pos not in self.index[token]:
                    match = False
                    break
            
            if match:
                results.append(first_pos)

        return results

    def get_word_distribution(self, language:str = None) -> Dict[str, int]:
        """
        Get word frequency distribution from the index.
        If language is specified, only count words from that language.
        Returns a dictionary mapping words to their frequency counts.
        """
        word_freq = Counter()

        for word, positions in self.index.items():
            if language:
                # Filter by language
                count = sum(1 for pos in positions if pos.language == language)
            else:
                count = len(positions)

            if count > 0:
                word_freq[word] = count

        return dict(word_freq)

    def get_top_words(self, n:int = 10, language:str = None) -> List[Tuple[str, int]]:
        """
        Get the top N most frequent words.
        If language is specified, only count words from that language.
        Returns a list of (word, count) tuples sorted by frequency.
        """
        distribution = self.get_word_distribution(language)
        return Counter(distribution).most_common(n)

    def process_single_document(self, filepath:str, language:str = 'en') -> Dict[str, int]:
        """
        Process a single document and return its word distribution without adding to index.
        This is useful for analyzing new documents against an existing corpus.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split into paragraphs and process
        paragraphs = content.split('\n\n')
        all_tokens = []

        for para in paragraphs:
            tokens = self.process_text(para, language)
            all_tokens.extend(tokens)

        # Create distribution
        return dict(Counter(all_tokens))

    def tag_document_with_language(self, filepath:str, language:str = 'en') -> None:
        """
        Process and index a single document with a specific language tag.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        filename = os.path.basename(filepath)
        paragraphs = content.split('\n\n')

        for i, para in enumerate(paragraphs):
            tokens = self.process_text(para, language)
            self.index_tokens(tokens, i, filename, language)






