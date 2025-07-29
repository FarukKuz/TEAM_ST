import json
from ai_core.utils import convert_to_english_chars
from ai_core.config import EXAM_DATA_FILEPATHS

def load_exam_data(exam_type: str) -> dict | None:
   
    filepath = EXAM_DATA_FILEPATHS.get(exam_type.upper())
    if not filepath:
        print(f"Hata: '{exam_type}' sınav tipi için yapılandırılmış veri dosyası bulunamadı.")
        return None

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Hata: '{filepath}' dosyası bulunamadı. Sınav tipi: '{exam_type}'.")
        return None
    except json.JSONDecodeError:
        print(f"Hata: '{filepath}' dosyası geçerli bir JSON formatında değil. Sınav tipi: '{exam_type}'.")
        return None

    grouped_data = {}
    data_list = raw_data.get(f"{exam_type.upper()}_DATA", raw_data) if isinstance(raw_data, dict) else raw_data

    for item in data_list:
        course_tr = item.get("ders")
        topic_tr = item.get("konu")

        if course_tr and topic_tr:
            course_en = convert_to_english_chars(course_tr)
            topic_en = convert_to_english_chars(topic_tr)

            if course_en not in grouped_data:
                grouped_data[course_en] = []
            if topic_en not in grouped_data[course_en]:
                grouped_data[course_en].append(topic_en)
    return grouped_data

_exam_data_cache = {}

def get_cached_exam_data(exam_type: str) -> dict | None:

    if exam_type not in _exam_data_cache:
        _exam_data_cache[exam_type] = load_exam_data(exam_type)
    return _exam_data_cache[exam_type]