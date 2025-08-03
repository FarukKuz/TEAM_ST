import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")

EXAM_DATA_FILEPATHS = {
    "TYT": os.path.join(os.path.dirname(__file__), "data", "tyt_data.json"),
    "KPSS": os.path.join(os.path.dirname(__file__), "data", "kpss_data.json"),
}

GEMINI_MODEL_NAME = 'gemini-2.0-flash'

GEMINI_VISION_MODEL_NAME = 'gemini-2.0-flash'