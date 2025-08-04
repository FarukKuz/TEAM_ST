import re

def convert_to_english_chars(text: str) -> str:
    replacements = {
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'İ': 'I',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def clean_gemini_response(response_text: str) -> str:
    text = response_text.strip()

    if text.startswith('```json'):
        # Remove the starting markdown and the closing '```'
        text = text[7:]  # '```json' is 7 characters long
        if text.endswith('```'):
            text = text[:-3]
    
    # If the response doesn't contain a JSON block, it might still have unwanted chars.
    # A simple strip is good for this case.
    # We remove any potential backticks that might have remained.
    text = text.strip('` \n')

    return text