import os

# Gemini API Anahtarı - ortam değişkeni olarak revize edilecek.
GEMINI_API_KEY = "AIzaSyCY39OmHpUqbM7Bg0Px9-tUJt1kTweHaHg"

EXAM_DATA_FILEPATHS = {
    "TYT": os.path.join(os.path.dirname(__file__), "data", "tyt_data.json"),
    "KPSS": os.path.join(os.path.dirname(__file__), "data", "kpss_data.json"),
}

GEMINI_MODEL_NAME = 'gemini-2.0-flash'

#added vision mode
GEMINI_VISION_MODEL_NAME = 'gemini-2.0-flash'