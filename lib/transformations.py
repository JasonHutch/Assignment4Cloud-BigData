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
        tokens = list(dict.fromkeys(tokens))
        
        return tokens, len(tokens)
    
    def List_all_starting_with(self, ref_string, all_words):
        """
        For each character in ref_string, list all words from all_words that begin with that character.
        Returns a list of tuples: [(char, [word1, word2, ...]), ...] preserving the order of first appearance
        of characters in ref_string. Comparison is case-insensitive; non-alphabetic characters are ignored.
        """
        result = []
        if not ref_string:
            return result

        # Normalize all_words into a list of strings (preserve original casing for output)
        if isinstance(all_words, str):
            words = re.findall(r"[A-Za-z']+", all_words)
        elif isinstance(all_words, (list, tuple, set)):
            words = [w for w in all_words if isinstance(w, str)]
        else:
            words = re.findall(r"[A-Za-z']+", str(all_words))

        seen = set()
        for ch in str(ref_string):
            cl = ch.lower()
            if cl in seen:
                continue
            seen.add(cl)
            if not cl.isalpha():
                continue
            matches = [w for w in words if w.lower().startswith(cl)]
            result.append((cl, matches))

        return result

    def Remove_stop_words_custom(self, stop_words_list: list, text_T: str, string_S: str = None) -> dict:
        """
        Remove custom stop words from text.

        Args:
            stop_words_list: List of stop words to remove (up to 10)
            text_T: The text to process
            string_S: Optional reference string (for future use)

        Returns:
            dict with keys:
                - 'removed_count': Number of stop words removed
                - 'resulting_text': Text after removing stop words
                - 'original_text': Original text
                - 'stop_words_used': List of stop words that were actually found and removed
        """
        # Limit to 10 stop words as per requirement
        stop_words_list = stop_words_list[:10] if len(stop_words_list) > 10 else stop_words_list

        # Convert stop words to lowercase for case-insensitive matching
        stop_words_set = set(word.lower().strip() for word in stop_words_list if word.strip())

        # Extract words from text while preserving structure
        words = re.findall(r"[A-Za-z']+", text_T)

        # Track removed words
        removed_count = 0
        removed_words = set()

        # Create a copy of the text to modify
        resulting_text = text_T

        # Remove stop words (case-insensitive)
        for word in words:
            if word.lower() in stop_words_set:
                # Use word boundary regex to replace whole words only
                pattern = r'\b' + re.escape(word) + r'\b'
                matches = re.findall(pattern, resulting_text, re.IGNORECASE)
                removed_count += len(matches)
                removed_words.add(word.lower())
                # Replace with empty string but keep punctuation/spacing
                resulting_text = re.sub(pattern, '', resulting_text, flags=re.IGNORECASE)

        # Clean up extra spaces
        resulting_text = re.sub(r'\s+', ' ', resulting_text).strip()
        # Clean up orphaned punctuation and spaces
        resulting_text = re.sub(r'\s+([.,!?;:])', r'\1', resulting_text)
        resulting_text = re.sub(r'([.,!?;:])\s*([.,!?;:])', r'\1', resulting_text)

        return {
            'removed_count': removed_count,
            'resulting_text': resulting_text,
            'original_text': text_T,
            'stop_words_used': sorted(list(removed_words))
        }





