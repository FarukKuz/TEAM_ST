from ai_core.topic_tagging_service import tag_question

class CurriculumService:
    def get_question_tags(self, question_text: str, exam_type: str) -> dict:
        return tag_question(question_text, exam_type)

# Örnek kullanım (backend API çağrısı gibi düşünebilirsin)
if __name__ == "__main__":
    service = CurriculumService()
    test_question_tyt = "Bir üçgende iç açılar toplamı kaçtır?"
    tags_tyt = service.get_question_tags(test_question_tyt, "TYT")
    print(f"Test Sorusu (TYT): {test_question_tyt}")
    print(f"Etiketler (TYT): {tags_tyt}")

    test_question_kpss = "Türkiye'nin en uzun akarsuyu hangisidir?"
    tags_kpss = service.get_question_tags(test_question_kpss, "KPSS")
    print(f"Test Sorusu (KPSS): {test_question_kpss}")
    print(f"Etiketler (KPSS): {tags_kpss}")