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
    cleaned = response_text.strip().split(',')[0].strip()
    return re.sub(r'^["\']|["\']$', '', cleaned)