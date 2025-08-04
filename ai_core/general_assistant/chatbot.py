import os
import io # Bu kütüphaneyi ekliyoruz, çünkü dosya baytlarını okumak için gerekli.
from ai_core.exam_data_loader import get_cached_exam_data
from ai_core.llm_service import get_llm_response_for_course, get_llm_response_for_topic, get_gemini_vision_response


def tag_question(question_text: str, exam_type: str) -> dict:
    """
    Tags a question with its course and topic based on the exam type.

    Args:
        question_text: The text of the question.
        exam_type: The type of the exam (e.g., "TYT").

    Returns:
        A dictionary containing the course, topic, and any potential errors.
    """
    exam_data = get_cached_exam_data(exam_type)

    if not exam_data:
        return {"course": "UNKNOWN", "topic": "UNKNOWN", "error": f"'{exam_type}' exam data could not be loaded. Please check the JSON file."}

    available_courses = list(exam_data.keys())

    # 1. Determine the course
    course = get_llm_response_for_course(question_text, available_courses)
    if course == "UNKNOWN":
        return {"course": "UNKNOWN", "topic": "UNKNOWN", "error": "Could not determine the course."}

    # 2. Get the topic list for the determined course
    topic_list_for_course = exam_data.get(course)
    if not topic_list_for_course:
        return {"course": course, "topic": "UNKNOWN", "error": f"No topic list found for the '{course}' course."}

    # 3. Determine the topic within the specific course's topics
    topic = get_llm_response_for_topic(question_text, course, topic_list_for_course)
    if topic == "UNKNOWN":
        return {"course": course, "topic": "UNKNOWN", "error": "Could not determine the topic."}

    return {"course": course, "topic": topic}


def process_questions_from_directory(directory_path: str, exam_type: str) -> None:
    """
    Reads question files from a directory, tags them, and prints the results.
    This version uses Gemini Vision for image files.
    """
    print(f"--- Processing questions from '{directory_path}' directory ---")
    
    try:
        filenames = sorted(os.listdir(directory_path))
    except FileNotFoundError:
        print(f"Error: Directory not found at '{directory_path}'.")
        return

    for filename in filenames:
        file_path = os.path.join(directory_path, filename)
        
        if not os.path.isfile(file_path) or filename.startswith('.'):
            continue

        question_text = ""
        file_extension = os.path.splitext(filename)[1].lower()

        print(f"\n--- Processing file: {filename} ---")

        try:
            if file_extension in ['.png', '.jpg', '.jpeg']:
                # Gemini Vision modelini kullanarak görseldeki metni çıkar
                with open(file_path, 'rb') as f:
                    image_bytes = f.read()

                # Gemini Vision'a sadece görseli gönderip metin çıkarmasını istiyoruz
                # Bunun için prompt'u uygun şekilde düzenleyebiliriz.
                # Örneğin, "Görseldeki soruyu metin olarak yaz."
                vision_prompt = "Görseldeki tüm metni, özellikle de sorunun kendisini tam olarak çıkar."
                vision_response_text = get_gemini_vision_response(image_bytes, vision_prompt)

                if not vision_response_text.strip():
                    print("Warning: Could not extract text from the image using Gemini Vision, skipping.")
                    continue
                
                question_text = vision_response_text
            else: # Diğer dosyaları metin olarak oku
                with open(file_path, 'r', encoding='utf-8') as file:
                    question_text = file.read().strip()
                    if not question_text:
                        print("Warning: File is empty, skipping.")
                        continue
            
            tagged_info = tag_question(question_text, exam_type)
            print(f"Tag: Course: {tagged_info['course']}, Topic: {tagged_info['topic']}")
            
            if "error" in tagged_info:
                print(f"  Error: {tagged_info['error']}")

        except Exception as e:
            print(f"Error processing '{filename}': {e}")


# Main execution block
if __name__ == "__main__":
    questions_folder = os.path.expanduser('~/Desktop/sorbi-sorular')
    exam_type_to_process = "TYT"
    process_questions_from_directory(questions_folder, exam_type_to_process)