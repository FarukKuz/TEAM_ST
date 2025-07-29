from ai_core.exam_data_loader import get_cached_exam_data
from ai_core.llm_service import get_llm_response_for_course, get_llm_response_for_topic


def tag_question(question_text: str, exam_type: str) -> dict:

    exam_data = get_cached_exam_data(exam_type)

    if not exam_data:
        return {"course": "UNKNOWN", "topic": "UNKNOWN", "error": f"'{exam_type}' sınav verileri yüklenemedi. JSON dosyasını kontrol edin."}

    available_courses = list(exam_data.keys())

    # 1. Dersi belirle
    course = get_llm_response_for_course(question_text, available_courses)
    if course == "UNKNOWN":
        return {"course": "UNKNOWN", "topic": "UNKNOWN", "error": "Ders belirlenemedi."}

    # 2. Belirlenen dersin konu listesini al
    topic_list_for_course = exam_data.get(course)
    if not topic_list_for_course:
        return {"course": course, "topic": "UNKNOWN", "error": f"'{course}' dersi için konu listesi bulunamadı."}

    # 3. Belirli dersin konuları içinde konuyu belirle
    topic = get_llm_response_for_topic(question_text, course, topic_list_for_course)
    if topic == "UNKNOWN":
        return {"course": course, "topic": "UNKNOWN", "error": "Konu belirlenemedi."}

    return {"course": course, "topic": topic}


# test için ----------------------------------
if __name__ == "__main__":
    print("--- Genel Sınav Sorusu Etiketleme Sonuçları ---")

    tyt_questions = [
        "Bir öğrenci 200 sayfalık bir kitabı okurken ilk gün 40 sayfa okuyor. Kalan sayfaları her gün bir önceki günden 10 sayfa fazla okuyarak bitiriyor. Kitabın tamamını kaç günde okumuştur?",
        "Aşağıdaki cümlelerin hangisinde virgülün kullanımı yanlıştır?",
        "Türkiye'de en yüksek dağ hangisidir?"
        """Tarihçilerin sıklıkla ifade ettiği üzere geçmişi anımsayamayanlar onu yinelemek durumunda kalır. Aşağıdakilerden hangisi bu cümle ile anlamca aynı doğrultudadır?
        A) Geçmişin mirası ancak sürekli hatırlatılarak canlı tutulur.
        B) Geçmişte yaşananlar zaman geçtikçe anlaşılabilir hâle gelir.
        C) Geçmiş ancak geleceğe uyarlanabildiği ölçüde değer kazanır.
        D) Geçmişten uzaklaşamayanlar eskiye saplanıp geleceği ıskalar.
        E) Geçmişte olanlar şimdiki zamana ve geleceğe kılavuzluk eder"""
    ]


    print("\n--- TYT Soruları ---")
    for i, question in enumerate(tyt_questions):
        print(f"\nSoru {i+1}: {question}")
        # Fonksiyon çağrısı güncellendi
        tagged_info = tag_question(question, "TYT")
        print(f"Etiket: Ders: {tagged_info['course']}, Konu: {tagged_info['topic']}")
        if "error" in tagged_info:
            print(f"  Hata: {tagged_info['error']}")
