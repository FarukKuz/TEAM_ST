import google.generativeai as genai
from ai_core.config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from ai_core.utils import clean_gemini_response

genai.configure(api_key=GEMINI_API_KEY)

LLM_MODEL = genai.GenerativeModel(GEMINI_MODEL_NAME)

# Ders belirlenir
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
        print(f"Gemini API Hatası (Ders belirleme): {e}")
        return "UNKNOWN"

# Belirlenen derse göre konu belirlenir. Yanıtlar kısıtlanmıştır. Şu an için sadce text olarak girdi almaktadır.
# !! Görsel düzenlemesi gerek !!
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
        print(f"Gemini API Hatası (Konu belirleme): {e}")
        return "UNKNOWN"