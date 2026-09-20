import re
import spacy

nlp = spacy.load("en_core_web_sm")

STOP_PHRASES = {"i", "you", "he", "she", "it", "we", "they", "this", "that", "these", "those", "who", "which"}


def extract_key_phrases(text: str, max_phrases: int = 60) -> list:
    text = text[:20000]
    doc = nlp(text)
    phrases = []
    seen = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        phrase = re.sub(r"^(a|an|the|your|our|their|his|her|my)\s+", "", phrase)
        word_count = len(phrase.split())
        if word_count < 2 or word_count > 5:
            continue
        if phrase in STOP_PHRASES or phrase in seen:
            continue
        if not re.search(r"[a-zA-Z]", phrase):
            continue
        seen.add(phrase)
        phrases.append(phrase)
        if len(phrases) >= max_phrases:
            break

    return phrases
