import os
import google.generativeai as genai

# API anahtarını terminalden alıyoruz
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Hata: GOOGLE_API_KEY ayarlanmamış. Lütfen terminalde 'export GOOGLE_API_KEY=\"ANAHTARINIZ\"' komutunu çalıştırın.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)

# Gemini modelini seç
model = genai.GenerativeModel('gemini-2.5-pro')

# Gemini'ye sorulacak soru
prompt = "Merhaba Gemini, nasılsın?"

try:
    # Yanıt al
    response = model.generate_content(prompt)
    print("Gemini'nin yanıtı:")
    print(response.text)
except Exception as e:
    print(f"Bir hata oluştu: {e}")