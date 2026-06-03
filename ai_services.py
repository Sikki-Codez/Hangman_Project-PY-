import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel

class WordList(BaseModel):
    words: list[str]

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialize Gemini Client: {e}")
        return None

def generate_words(category_name, word_count=100, min_len=5, max_len=20):
    client = get_client()
    if not client:
        raise Exception("Gemini Client not initialized. Please set GEMINI_API_KEY in the environment.")
    
    prompt = f"""
    Provide exactly {word_count} unique words related to the category '{category_name}'.
    Rules:
    1. Every word must be between {min_len} and {max_len} letters long.
    2. Only use alphabetical characters (no numbers, spaces, or hyphens).
    """
    
    try:
        # Use structured outputs with a Pydantic schema for maximum reliability
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=WordList,
            )
        )
        
        raw_text = response.text.strip()
        data = json.loads(raw_text)
        words = data.get("words", [])
        
        # Clean and filter
        valid_words = []
        for word in words:
            w = str(word).lower().strip()
            if w.isalpha() and min_len <= len(w) <= max_len:
                valid_words.append(w)
                
        return list(set(valid_words))
        
    except Exception as e:
        print(f"Error in generate_words: {e}")
        raise e

def generate_hint(word, guessed_letters):
    client = get_client()
    if not client:
        return "Clue unavailable (AI key not set)."
    
    guessed_str = ", ".join(guessed_letters) if guessed_letters else "none"
    prompt = f"""
    The user is playing a game of Hangman.
    The secret word is: "{word}"
    The letters they have guessed so far are: {guessed_str}
    
    Provide a short, cryptic, semantic clue (maximum 10 words) that helps the player guess the word without revealing the word itself or spelling it.
    Do not include the word "{word}" in the clue. Keep the explanation very brief and enigmatic.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating hint: {e}")
        return "Could not generate a hint at this moment."
