import os
import string
import re

class Transformations:
    def __init__(self):
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

    def remove_stop_words(self,input_string:str) -> str:
        tokens = re.findall(r"[A-Za-z']+", input_string.lower())
        filtered = [t for t in tokens if t not in self.STOP_WORDS]

        return filtered
    
    def remove_puncuation(self, input_text:str) -> str:
        translator = str.maketrans('','',string.punctuation)
        cleaned_text = input_text.translate(translator)
        
        return cleaned_text