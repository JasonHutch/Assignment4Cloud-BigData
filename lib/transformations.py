import os
import string
import re

class Transformations:
    def __init__(self):
        self.STOP_WORDS_EN = {
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

        self.STOP_WORDS_FR = {
            "le", "la", "les", "un", "une", "des", "de", "du", "à", "au", "aux",
            "et", "ou", "mais", "donc", "or", "ni", "car", "ce", "cet", "cette",
            "ces", "mon", "ton", "son", "ma", "ta", "sa", "mes", "tes", "ses",
            "notre", "votre", "leur", "nos", "vos", "leurs", "je", "tu", "il",
            "elle", "nous", "vous", "ils", "elles", "me", "te", "se", "moi",
            "toi", "lui", "eux", "qui", "que", "quoi", "dont", "où", "dans",
            "sur", "sous", "avec", "sans", "pour", "par", "en", "vers", "chez",
            "être", "avoir", "faire", "dire", "aller", "voir", "savoir", "pouvoir",
            "vouloir", "venir", "falloir", "devoir", "croire", "trouver", "donner",
            "prendre", "parler", "aimer", "passer", "mettre", "est", "sont", "était",
            "étaient", "sera", "seront", "été", "ai", "as", "a", "avons", "avez",
            "ont", "avait", "avaient", "aura", "auront", "eu", "suis", "es",
            "sommes", "êtes", "puis", "peut", "peuvent", "d", "l", "c", "s",
            "n", "m", "t", "j", "qu", "y", "si", "ne", "pas", "plus", "tous",
            "tout", "toute", "toutes", "autre", "autres", "même", "mêmes", "tel",
            "telle", "tels", "telles", "quel", "quelle", "quels", "quelles"
        }

        self.STOP_WORDS = self.STOP_WORDS_EN  # Default to English

    def remove_stop_words(self,input_string:str, language:str = 'en') -> str:
        # Select appropriate stop words based on language
        stop_words = self.STOP_WORDS_FR if language == 'fr' else self.STOP_WORDS_EN

        # For French, include accented characters in regex
        if language == 'fr':
            tokens = re.findall(r"[A-Za-zÀ-ÿ']+", input_string.lower())
        else:
            tokens = re.findall(r"[A-Za-z']+", input_string.lower())

        filtered = [t for t in tokens if t not in stop_words]

        return filtered
    
    def remove_puncuation(self, input_text:str) -> str:
        translator = str.maketrans('','',string.punctuation)
        cleaned_text = input_text.translate(translator)
        
        return cleaned_text
    
    def Count_num_chars(self, ref_string: str, input_string: str) -> str:
        """
        Count the total number of each char from S in T
        """
        char_freq = dict()

        # inital counts for chars in ref_string
        for char in ref_string:
            if char not in char_freq:
                char_freq[char] = 0

        # count occurrences in input_string
        for char in input_string:
            if char in char_freq:
                char_freq[char] += 1

        return char_freq
                
    def Count_freq_chars(self, input_string:str, char_count) -> str:
        """
        Get the freqeunce of each char from S in T
        """
        char_freq = char_count.copy()
        input_length = len(input_string)
        
        for key,value in char_freq.items():
            char_freq[key] = value / input_length
            
        return char_freq
  
    def Replace_with_char(self,char:str, input_string:str, char_count) -> str:
        """
        Find every character in T that is also present in S, and replace all those characters with the single character C that you are given.
        """

        for key, value in char_count.items():
            if value > 0:
                input_string = input_string.replace(key, char)

        return input_string
    
    
    
    def List_all_words(self, input_string:str) -> str:
        tokens = re.findall(r"[A-Za-z']+", input_string.lower())
        return tokens
        
        