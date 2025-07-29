import google.generativeai as genai
from ai_core.config import GEMINI_API_KEY, GEMINI_MODEL_NAME, EXAM_DATA_FILEPATHS
from ai_core.topic_tagging_service import tag_question
from ai_core.llm_service import LLM_MODEL

genai.configure(api_key=GEMINI_API_KEY)

def get_assistant_response(user_query: str) -> str:

    detected_tags = {"course": "UNKNOWN", "topic": "UNKNOWN"}

    # Kullanici seçmeli. Soruyu gönderebilmek için belirlemek zorunda.
    default_exam_type = "TYT"
    
    # Kullanıcı sorgusunda sınav tipi belirtilmiş mi kontrol et
    # Basit bir kontrol, daha gelişmiş NLP gerekebilir.
    for exam_type_key in EXAM_DATA_FILEPATHS.keys():
        if exam_type_key.lower() in user_query.lower():
            default_exam_type = exam_type_key
            break

    tags_result = tag_question(user_query, default_exam_type)
    
    detected_course = tags_result.get("course", "UNKNOWN")
    detected_topic = tags_result.get("topic", "UNKNOWN")
    tag_error = tags_result.get("error")

    general_prompt = (
        f"Kullanıcının aşağıdaki sorusuna detaylı ve yardımcı bir yanıt ver. "
        f"Sorunun konusu ve dersi tespit edildiyse, cevabına bu bilgiyi de ekleyebilirsin.\n\n"
        f"Tespit Edilen Ders: {detected_course}\n"
        f"Tespit Edilen Konu: {detected_topic}\n"
        f"Kullanıcı Sorusu: {user_query}"
    )

    try:
        response = LLM_MODEL.generate_content(general_prompt)
        assistant_reply = response.text
    except Exception as e:
        assistant_reply = f"Üzgünüm, şu an bir yanıt oluşturamıyorum. Bir sorun oluştu: {e}"

    tag_info = ""
    if detected_course != "UNKNOWN" or detected_topic != "UNKNOWN":
        tag_info = f"\n\n(Bu soruyu '{detected_course}' dersinin '{detected_topic}' konusuna ait olarak etiketledim.)"
    elif tag_error:
        tag_info = f"\n\n(Sorunun dersini/konusunu belirlerken bir sorun oluştu: {tag_error})"


    return assistant_reply + tag_info

def start_chatbot_terminal_interface():

    print("Merhaba! Ben senin sınav asistanınım. Hangi konuda yardıma ihtiyacın var?")
    print("Çıkmak için 'çıkış' yazabilirsin.")

    while True:
        user_input = input("\nSen: ")
        if user_input.lower() in ["çıkış", "exit", "quit"]:
            print("Görüşmek üzere!")
            break

        print("Asistan düşünüyor...")
        response = get_assistant_response(user_input)
        print(f"Asistan: {response}")

if __name__ == "__main__":
    start_chatbot_terminal_interface()