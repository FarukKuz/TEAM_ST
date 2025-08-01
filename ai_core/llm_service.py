# exam-assistant-app/ai_core/llm_service.py
import google.generativeai as genai
from PIL import Image # Pillow kütüphanesinden Image import edildi
import io # Bellekte görsel verisi işlemek için

from ai_core.config import GEMINI_API_KEY, GEMINI_MODEL_NAME, GEMINI_VISION_MODEL_NAME
from ai_core.utils import clean_gemini_response

# Gemini API'sini yapılandır
genai.configure(api_key=GEMINI_API_KEY)

LLM_MODEL = genai.GenerativeModel(GEMINI_MODEL_NAME)

VISION_LLM_MODEL = genai.GenerativeModel(GEMINI_VISION_MODEL_NAME)

def get_llm_response_for_course(question_text: str, available_courses: list) -> str | None:

    courses_str = ", ".join(available_courses)
    prompt = (
        f"Aşağıdaki sorunun hangi derse ait olduğunu belirle. Cevabın SADECE şu derslerden biri olmalı "
        f"ve başka hiçbir şey olmamalı: {courses_str}.\n"
        f"Eğer kesin olarak belirleyemezsen 'UNKNOWN' olarak cevapla.\n\n"
        f"Soru: {question_text}"
    )
    try:
        response = LLM_MODEL.generate_content(prompt)
        predicted_course = clean_gemini_response(response.text)

        for course in available_courses:
            if course.upper() == predicted_course.upper():
                return course
        return "UNKNOWN"
    except Exception as e:
        return f"Gemini API Hatası (Ders belirleme): {e}"

def get_llm_response_for_topic(question_text: str, parent_course: str, available_topics: list) -> str | None:

    topics_str = ", ".join(available_topics)
    prompt = (
        f"'{parent_course}' dersi içinde, aşağıdaki sorunun hangi konuya ait olduğunu belirle. "
        f"Cevabın SADECE şu konulardan biri olmalı ve başka hiçbir şey olmamalı: {topics_str}.\n"
        f"Eğer kesin olarak belirleyemezsen 'UNKNOWN' olarak cevapla.\n\n"
        f"Soru: {question_text}"
    )
    try:
        response = LLM_MODEL.generate_content(prompt)
        predicted_topic = clean_gemini_response(response.text)

        for topic in available_topics:
            if topic.lower() == predicted_topic.lower():
                return topic
        return "UNKNOWN"
    except Exception as e:
        return f"Gemini API Hatası (Konu belirleme): {e}"

def get_gemini_vision_response(image_bytes: bytes, text_prompt: str = "") -> str:
    """
    Gemini Vision modeline bir görsel ve isteğe bağlı bir metin sorgusu gönderir
    ve modelin görselle ilgili metin yanıtını döndürür.

    Args:
        image_bytes: Görselin bayt dizisi (örneğin, bir dosya okunduğunda elde edilen).
        text_prompt: Görselle birlikte gönderilecek metin sorgusu (örn: "Bu resimde ne var?",
                     "Bu matematik problemi ne ile ilgili?", "Soruyu çöz.").

    Returns:
        Gemini'den gelen metin yanıtı veya bir hata mesajı.
    """
    try:
        # Görselin MIME tipini belirle. Genellikle JPEG veya PNG kullanılır.
        # Basitlik için burada sabit 'image/jpeg' kullanıldı.
        # Gerçek uygulamada, dosya uzantısına göre dinamik olarak belirlenebilir.
        image_part = {
            'mime_type': 'image/jpeg', # Yüklediğin görselin gerçek MIME tipini burada belirtmelisin (png, jpeg vb.)
            'data': image_bytes
        }

        contents = [image_part]
        if text_prompt:
            contents.append(text_prompt)

        response = VISION_LLM_MODEL.generate_content(contents)
        return response.text
    except Exception as e:
        return f"Gemini Vision API hatası: {e}"