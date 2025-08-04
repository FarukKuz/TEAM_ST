import google.generativeai as genai
from PIL import Image
import io
import os

from ai_core.config import GEMINI_MODEL_NAME, GEMINI_VISION_MODEL_NAME
from ai_core.utils import clean_gemini_response

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
    try:
        image_part = {
            'mime_type': 'image/png', # Yüklediğin görselin tipi
            'data': image_bytes
        }

        contents = [image_part]
        if text_prompt:
            contents.append(text_prompt)

        response = VISION_LLM_MODEL.generate_content(contents)
        return response.text
    except Exception as e:
        return f"Gemini Vision API hatası: {e}"