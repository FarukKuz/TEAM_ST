import os

# Gemini API Anahtarı - ortam değişkeni olarak revize edilecek.
GEMINI_API_KEY = "AIzaSyB8FORnRdmQzhftnvDLpAMiJsMUv_AdNK4"

EXAM_DATA_FILEPATHS = {
    "TYT": os.path.join(os.path.dirname(__file__), "data", "tyt_data.json"),
    "KPSS": os.path.join(os.path.dirname(__file__), "data", "kpss_data.json"),
}

GEMINI_MODEL_NAME = 'gemini-2.0-flash'