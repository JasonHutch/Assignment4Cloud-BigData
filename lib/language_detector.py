"""
Language Detector Module
This module provides functionality to detect the language of text by comparing
word distributions against reference language models built from document corpora.
"""

import os
from typing import Dict, List, Optional, Tuple
from collections import Counter
from lib.transformations import Transformations


class LanguageDetector:
    """
    A class for building language models from document collections and
    detecting the language of input text by comparing word distributions.
    """

    def __init__(self):
        """Initialize the LanguageDetector with transformation utilities."""
        self.transformations = Transformations()
        self.language_models: Dict[str, Dict[str, int]] = {}

        self.build_language_model('resources/CandideFr.txt', 'fr')
        self.build_language_model('resources/CandideEn.txt', 'en')

    def build_language_model(self, documents_path: str, language: str) -> None:
        """
        Build a word distribution model for a specific language from document(s).

        Args:
            documents_path: Path to a file or directory containing documents
            language: Language code (e.g., 'en', 'fr')

        Raises:
            FileNotFoundError: If the path doesn't exist
        """
        if not os.path.exists(documents_path):
            raise FileNotFoundError(f"Path not found: {documents_path}")

        all_tokens = []

        # Handle single file
        if os.path.isfile(documents_path):
            all_tokens.extend(self._process_document(documents_path, language))

        # Handle directory
        elif os.path.isdir(documents_path):
            for filename in os.listdir(documents_path):
                if filename.endswith('.txt'):
                    filepath = os.path.join(documents_path, filename)
                    all_tokens.extend(self._process_document(filepath, language))

        # Build distribution
        distribution = dict(Counter(all_tokens))
        self.language_models[language] = distribution

    def _process_document(self, filepath: str, language: str) -> List[str]:
        """
        Process a single document and return its tokens.

        Args:
            filepath: Path to the document
            language: Language code for processing

        Returns:
            List of processed tokens
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # Process text using language-specific rules
        content = content.lower()

        # Preserve accented characters for French
        if language != 'fr':
            content = ''.join(c for c in content if ord(c) < 127)

        # Remove punctuation
        content = self.transformations.remove_puncuation(content)

        # Remove stop words and tokenize
        tokens = self.transformations.remove_stop_words(content, language)

        return tokens

    def get_distribution_from_text(self, text: str, language: Optional[str] = None) -> Dict[str, int]:
        """
        Get word distribution from text content.

        Args:
            text: Text content to analyze
            language: Language code for processing (optional, uses 'en' by default)

        Returns:
            Dictionary mapping words to their frequency counts
        """
        if language is None:
            language = 'en'

        # Process text using language-specific rules
        content = text.lower()

        # Preserve accented characters for French
        if language != 'fr':
            content = ''.join(c for c in content if ord(c) < 127)

        # Remove punctuation
        content = self.transformations.remove_puncuation(content)

        # Remove stop words and tokenize
        tokens = self.transformations.remove_stop_words(content, language)

        return dict(Counter(tokens))

    def calculate_similarity(self, dist1: Dict[str, int], dist2: Dict[str, int]) -> float:
        """
        Calculate similarity between two word distributions using cosine similarity.

        Args:
            dist1: First word distribution
            dist2: Second word distribution

        Returns:
            Similarity score between 0 and 1 (1 = identical)
        """
        # Get common words
        all_words = set(dist1.keys()) | set(dist2.keys())

        if not all_words:
            return 0.0

        # Calculate cosine similarity
        dot_product = sum(dist1.get(word, 0) * dist2.get(word, 0) for word in all_words)

        magnitude1 = sum(count ** 2 for count in dist1.values()) ** 0.5
        magnitude2 = sum(count ** 2 for count in dist2.values()) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def detect_language(self, input_distribution: Dict[str, int],
                       threshold: float = 0.3,
                       return_details: bool = False) -> Tuple[Optional[str], float, Dict[str, float]] | Optional[str]:
        """
        Detect the language of an input distribution by comparing against stored models.

        Args:
            input_distribution: Word distribution to classify
            threshold: Minimum similarity score to consider a match (default: 0.3)
            return_details: If True, returns (language, score, all_scores).
                          If False, returns just the language code (default: False)

        Returns:
            If return_details=True: Tuple of (detected_language, confidence_score, all_scores)
            If return_details=False: Just the detected language code (or None)
            Returns None (or (None, 0.0, scores)) if no language meets the threshold
        """
        if not self.language_models:
            raise ValueError("No language models available. Build models first using build_language_model()")

        scores = {}

        # Calculate similarity with each language model
        for language, model_dist in self.language_models.items():
            similarity = self.calculate_similarity(input_distribution, model_dist)
            scores[language] = similarity

        # Find best match
        best_language = max(scores, key=scores.get)
        best_score = scores[best_language]

        detected = best_language if best_score >= threshold else None

        if return_details:
            return detected, best_score, scores
        else:
            return detected
