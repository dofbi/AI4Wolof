#import os
import csv
import time
from typing import Dict, List, Tuple
from difflib import SequenceMatcher
import re
from pydantic_ai import Agent
# from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
from pathlib import Path
from threading import Lock

# Constantes pour les valeurs par défaut et les configurations
DEFAULT_MODEL_NAME = "gemini-1.5-flash"
DEFAULT_MAX_LINES = 138  # Utiliser None pour traiter tout le fichier
DEFAULT_RETRY_DELAY = 5 # Délai en secondes entre les tentatives de l'appel à l'api
MAX_API_CALLS_PER_MINUTE = 15  # Nombre maximal d'appels API par minute

class RateLimiter:
    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = Lock()

    def __enter__(self):
        with self.lock:
            now = time.time()
            self.calls = [t for t in self.calls if t > now - self.period]
            while len(self.calls) >= self.max_calls:
                  time.sleep(0.1)  # Petite pause pour ne pas monopoliser le CPU
                  now = time.time()
                  self.calls = [t for t in self.calls if t > now - self.period]
            self.calls.append(now)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class SimpleMetricEvaluator:
    """
    Evaluates the quality of a translated text based on semantic similarity,
    length ratio, and exact match with a reference text.
    """
    def __init__(self):
        """Initializes the evaluator with stop words and semantic equivalences."""
        self.stop_words = {
            'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'je', 'tu', 'il', 'elle',
            'nous', 'vous', 'ils', 'elles', 'ce', 'ça', 'et', 'ou', 'à', 'au', 'aux',
            'en', 'dans', 'par', 'pour', 'sur', '?', '.', ',', '!'
        }
        self.semantic_equivalences = {
            'mangui gui fi': ['je suis là', 'je vais bien'],
            'kay gnou': ['allons', 'viens on'],
            'na nga def': ['comment vas-tu', 'comment allez-vous']
        }

    def preprocess(self, text: str) -> str:
        """
        Lowercase a text, remove punctuation, and strip whitespaces.
        
        Args:
            text: The input string.
        Returns:
            The preprocessed string.
        """
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()

    def word_similarity(self, word1: str, word2: str) -> float:
        """
         Computes the similarity between two words.
         
        Args:
            word1: The first word.
            word2: The second word.
            
        Returns:
            The similarity score.
        """
        return SequenceMatcher(None, word1, word2).ratio()

    def get_words(self, text: str) -> List[str]:
       """
       Extracts words from text, filtering out stop words.
      
       Args:
         text: The input text.
       Returns:
        A list of words.
      """
       return [word for word in text.split() if word not in self.stop_words]

    def semantic_similarity(self, ref_words: List[str], hyp_words: List[str]) -> float:
        """
        Calculates the semantic similarity between two lists of words.

        Args:
           ref_words: List of words from the reference text.
           hyp_words: List of words from the hypothesis text.
        Returns:
             The semantic similarity score.
        """
        if not ref_words or not hyp_words:
            return 0.0

        total_sim = 0
        for ref_word in ref_words:
            word_sims = [self.word_similarity(ref_word, hyp_word) for hyp_word in hyp_words]
            if word_sims:
                total_sim += max(word_sims)

        return total_sim / len(ref_words)

    def length_ratio(self, ref_words: List[str], hyp_words: List[str]) -> float:
        """
        Computes the length ratio between two word lists.
        
        Args:
           ref_words: List of words from the reference text.
           hyp_words: List of words from the hypothesis text.
           
        Returns:
          The length ratio.
        """
        if not ref_words:
            return 0.0
        return min(len(hyp_words) / len(ref_words), len(ref_words) / len(hyp_words))

    def evaluate(self, reference: str, hypothesis: str) -> Dict[str, float]:
        """
        Evaluates the translation hypothesis against a reference.

        Args:
           reference: The reference text.
           hypothesis: The translated text.
        Returns:
           A dictionary containing evaluation metrics.
        """
        ref = self.preprocess(reference)
        hyp = self.preprocess(hypothesis)

        ref_words = self.get_words(ref)
        hyp_words = self.get_words(hyp)

        sem_sim = self.semantic_similarity(ref_words, hyp_words)
        len_ratio = self.length_ratio(ref_words, hyp_words)
        exact_match = float(ref == hyp)

        final_score = (
            0.7 * sem_sim +
            0.2 * len_ratio +
            0.1 * exact_match
        )

        return {
            'score_final': final_score,
            'similarite_semantique': sem_sim,
            'ratio_longueur': len_ratio,
            'correspondance_exacte': exact_match
        }

class TranslationService:
    """Handles translation and evaluation using an AI agent."""
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        """Initializes the service with the specified model."""
        load_dotenv()

        # model = OpenAIModel(
        #     model_name,
        #     base_url='https://openrouter.ai/api/v1',
        #     api_key=os.environ.get("OPENROUTER_API_KEY"),
        # )
        
        self.translation_agent = Agent(
            model_name,
            deps_type=dict,
            result_type=str,
            system_prompt=(
                'Vous êtes un traducteur expert en Wolof et Français. '
                'Votre rôle est de traduire des phrases du Wolof vers le Français. '
                'Vous devez fournir une traduction, une seule claire et précise pour chaque phrase.'
            ),
        )
        self.evaluator = SimpleMetricEvaluator()
        self.rate_limiter = RateLimiter(MAX_API_CALLS_PER_MINUTE, 60)  # 60 seconds for 1 minute

    def translate_and_evaluate(self, wolof_phrase: str, reference_translation: str,
                             max_retries: int = 3, delay: int = DEFAULT_RETRY_DELAY) -> Tuple[str, Dict[str, float]]:
        """
        Translates a wolof phrase and evaluates the translation.
       
        Args:
             wolof_phrase: The wolof phrase to translate.
             reference_translation: The reference translation.
             max_retries: The maximum number of retries in case of failure.
             delay: The delay between retries.
        Returns:
           A tuple containing the translation and evaluation scores.
        """
        for attempt in range(max_retries):
            try:
                with self.rate_limiter:
                    result = self.translation_agent.run_sync(wolof_phrase)
                    translation = result.data.strip()
                    scores = self.evaluator.evaluate(reference_translation, translation)
                    return translation, scores

            except Exception as e:
                if "RESOURCE_EXHAUSTED" in str(e) and attempt < max_retries - 1:
                    print(f"Quota API atteint, tentative {attempt + 1}/{max_retries} dans {delay} secondes...")
                    time.sleep(delay)
                else:
                    raise e

class CSVProcessor:
    """Processes CSV files by translating and evaluating each row."""
    def __init__(self, translation_service: TranslationService):
        """Initializes with a translation service."""
        self.translation_service = translation_service

    def process_file(self, input_file: Path, output_file: Path, max_lines: int = None) -> None:
        """
        Processes the input CSV file and writes results to the output file.

       Args:
           input_file: The path to the input CSV file.
           output_file: The path to the output CSV file.
           max_lines: The maximum number of lines to process.
       """
        output_file.parent.mkdir(parents=True, exist_ok=True)
        total_score = 0
        count = 0

        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', newline='', encoding='utf-8') as f_out:
            
            reader = csv.DictReader(f_in)
            # Garder seulement les champs nécessaires dans le CSV
            fieldnames = ['No', 'Wolof', 'Français', 'Traduction', 'Score_Final']
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for i, row in enumerate(reader):
                if max_lines and i >= max_lines:
                    break
                
                print(f"Traitement de la ligne {i + 1}")
                translation, scores = self.translation_service.translate_and_evaluate(
                    row['Wolof'], row['Français']
                )

                writer.writerow({
                    'No': row['No'],
                    'Wolof': row['Wolof'],
                    'Français': row['Français'],
                    'Traduction': translation,
                    'Score_Final': f"{scores['score_final']:.3f}",
                   # 'Similarite_Semantique': f"{scores['similarite_semantique']:.3f}",
                   # 'Ratio_Longueur': f"{scores['ratio_longueur']:.3f}",
                   # 'Correspondance_Exacte': f"{scores['correspondance_exacte']:.3f}"
                })
                
                print(f"Scores pour la ligne {i + 1}:")
                print(f"Score final: {scores['score_final']:.3f}")
                # Pour afficher les autres scores, décommentez les lignes suivantes:
                #print(f"Similarité sémantique: {scores['similarite_semantique']:.3f}")
                #print(f"Ratio de longueur: {scores['ratio_longueur']:.3f}")
                #print(f"Correspondance exacte: {scores['correspondance_exacte']:.3f}")
                print("-" * 50)

                total_score += scores['score_final']
                count += 1
        
        if count > 0 :
            average_score = total_score / count
            print(f"\nMoyenne des scores finals: {average_score:.3f}")
        else:
            print("\nAucune ligne traitée, impossible de calculer la moyenne des scores.")
    
def main():
    """Main function to run the CSV processing."""
    input_file = Path('data/input/waxtane.csv')
    output_file = Path('data/output/traduction/traduction_evaluee.csv')
    
    translation_service = TranslationService()
    csv_processor = CSVProcessor(translation_service)
    
    try:
        csv_processor.process_file(input_file, output_file, max_lines=DEFAULT_MAX_LINES)
        print(f"Traitement terminé, résultats enregistrés dans '{output_file}'")
    except Exception as e:
        print(f"Erreur lors de l'exécution: {str(e)}")
        raise

if __name__ == "__main__":
    main()