# exam-assistant-app/ai_core/general_assistant/chatbot.py

import google.generativeai as genai
from PIL import Image # Pillow kütüphanesinden Image import edildi
import io # Bellekte görsel verisi işlemek için
import os # Dosya yolu işlemleri için

from ai_core.config import GEMINI_API_KEY, GEMINI_MODEL_NAME, EXAM_DATA_FILEPATHS
from ai_core.topic_tagging_service import tag_question # Soru etiketleme fonksiyonumuz
# LLM_MODEL ve VISION_LLM_MODEL doğrudan llm_service'ten import ediliyor
from ai_core.llm_service import LLM_MODEL, VISION_LLM_MODEL, get_gemini_vision_response # get_gemini_vision_response de eklendi

# Gemini API'sini yapılandır (emin olmak için burada da konfigüre edilebilir)
genai.configure(api_key=GEMINI_API_KEY)

def get_assistant_response(user_query: str, image_path: str = None) -> str:
    """
    Kullanıcı sorgusuna genel bir yanıt üretir ve soruyu etiketlemeye çalışır.
    İsteğe bağlı olarak bir görsel dosya yolu da alabilir.
    """
    detected_course = "UNKNOWN"
    detected_topic = "UNKNOWN"
    tag_error = None
    assistant_reply_parts = [] # Yanıt parçalarını bir liste olarak tutacağız
    text_for_tagging = user_query # Etiketleme için varsayılan metin

    # 1. Görsel varsa, Gemini Vision ile analiz et
    if image_path:
        if not os.path.exists(image_path):
            return f"Hata: Belirtilen görsel yolu bulunamadı: {image_path}"
        
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            # Görsel analizini yap
            vision_response_text = get_gemini_vision_response(image_bytes, user_query)
            assistant_reply_parts.append(f"Görsel analizi: {vision_response_text}")

            # Eğer Gemini Vision'dan anlamlı bir metin geldiyse, etiketlemede onu kullan
            if vision_response_text and "hata" not in vision_response_text.lower():
                # Kullanıcının metin sorgusu da varsa, ikisini birleştirerek etiketle
                text_for_tagging = vision_response_text + (" " + user_query if user_query else "")
            
        except Exception as e:
            assistant_reply_parts.append(f"Görsel işlenirken bir hata oluştu: {e}")
            tag_error = f"Görsel işleme hatası: {e}"

    # Kullanıcı belirlemeli
    default_exam_type = "TYT"
    # Kullanıcı sorgusunda sınav tipi belirtilmiş mi kontrol et (basitçe)
    for exam_type_key in EXAM_DATA_FILEPATHS.keys():
        if exam_type_key.lower() in user_query.lower():
            default_exam_type = exam_type_key
            break

    tags_result = tag_question(text_for_tagging, default_exam_type)
    detected_course = tags_result.get("course", "UNKNOWN")
    detected_topic = tags_result.get("topic", "UNKNOWN")
    tag_error = tags_result.get("error") if tag_error else tags_result.get("error") # Önceki hatayı koru veya yeni hatayı al

    # 3. Genel bir asistan yanıtı oluştur (metin tabanlı Gemini kullanarak)
    # Eğer asistan yanıtı görsel analizinden gelmediyse, genel metin yanıtı oluştur
    if not assistant_reply_parts: # Eğer hiç yanıt yoksa
        general_prompt = (
            f"Kullanıcının aşağıdaki sorusuna detaylı ve yardımcı bir yanıt ver. "
            f"Sorunun konusu ve dersi tespit edildiyse, cevabına bu bilgiyi de ekleyebilirsin.\n\n"
            f"Tespit Edilen Ders: {detected_course}\n"
            f"Tespit Edilen Konu: {detected_topic}\n"
            f"Kullanıcı Sorusu: {user_query}"
        )
        try:
            response = LLM_MODEL.generate_content(general_prompt)
            assistant_reply_parts.append(response.text)
        except Exception as e:
            assistant_reply_parts.append(f"Üzgünüm, şu an bir yanıt oluşturamıyorum. Bir sorun oluştu: {e}")

    # Etiketleme bilgisini yanıta ekle
    tag_info = ""
    if detected_course != "UNKNOWN" or detected_topic != "UNKNOWN":
        tag_info = f"\n\n(Bu soruyu '{detected_course}' dersinin '{detected_topic}' konusuna ait olarak etiketledim.)"
    elif tag_error:
        tag_info = f"\n\n(Sorunun dersini/konusunu belirlerken bir sorun oluştu: {tag_error})"

    return "\n".join(assistant_reply_parts) + tag_info

def start_chatbot_terminal_interface():
    """
    Terminalden kullanıcı ile etkileşime giren sohbet botu arayüzünü başlatır.
    Görsel yolu girişi için komutları destekler.
    """
    print("Merhaba! Ben senin sınav asistanınım. Hangi konuda yardıma ihtiyacın var?")
    print("Çıkmak için 'çıkış' yazabilirsin.")
    print("Görsel göndermek için 'görsel: [dosya_yolu] [metin_sorgusu]' formatını kullan.")
    print("Örnek: görsel: /Users/faruk/Desktop/soru.jpg Bu görseldeki matematik problemi nedir?")

    while True:
        user_input = input("\nSen: ")
        if user_input.lower() in ["çıkış", "exit", "quit"]:
            print("Görüşmek üzere!")
            break

        image_path = None
        text_query = user_input

        # Görsel girişi mi var kontrol et
        if user_input.lower().startswith("görsel:"):
            parts = user_input[len("görsel:"):].strip().split(" ", 1)
            if len(parts) >= 1:
                image_path = parts[0] # İlk kısım dosya yolu
                if len(parts) > 1:
                    text_query = parts[1] # İkinci kısım metin sorgusu
                else:
                    text_query = "" # Sadece görsel var, metin yok
            else:
                print("Hata: Görsel formatı yanlış. 'görsel: [dosya_yolu] [metin_sorgusu]' şeklinde olmalı.")
                continue

        print("Asistan düşünüyor...")
        response = get_assistant_response(text_query, image_path)
        print(f"Asistan: {response}")

# Bu dosya doğrudan çalıştırıldığında sohbet arayüzünü başlatır
if __name__ == "__main__":
    start_chatbot_terminal_interface()