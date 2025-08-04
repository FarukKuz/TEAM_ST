import os
import json
import io
from PIL import Image
import google.generativeai as genai

from ai_core.llm_service import LLM_MODEL, VISION_LLM_MODEL, get_gemini_vision_response
from ai_core.utils import clean_gemini_response

def generate_similar_question(original_question_text: str, original_image_bytes: bytes = None) -> dict:
    """
    Generates a new, similar question and its options based on an original question.
    It can use text from an image or a simple text prompt.

    Args:
        original_question_text: The text of the original question.
        original_image_bytes: The byte data of the original image (optional).

    Returns:
        A dictionary containing the new question, options, and the correct answer.
        Returns None if the generation fails.
    """

    # If image bytes are provided, get the text from the image first.
    if original_image_bytes:
        vision_prompt = (
            "Görseldeki soruyu, tüm şıkları ve doğru cevabı ayırarak tam olarak metin olarak çıkar. "
            "Cevap formatı şöyle olmalı: 'Soru: ...\nA) ...\nB) ...\nC) ...\nD) ...\nE) ...\nCevap: ...'"
        )
        original_text_from_vision = get_gemini_vision_response(original_image_bytes, vision_prompt)
        
        if not original_text_from_vision.strip():
            print("Warning: Could not extract text from the image using Gemini Vision.")
            if not original_question_text.strip():
                return None
        else:
            original_question_text = original_text_from_vision

    prompt = f"""
    Aşağıdaki soru ve şıklarına benzer yeni bir soru ve 4 yanlış, 1 doğru şık oluştur. 
    Yeni soru, orijinal sorunun konusu ve zorluk seviyesine yakın olmalıdır.
    Cevap formatı kesinlikle bir JSON nesnesi olmalıdır ve başka hiçbir metin içermemelidir.
    JSON yapısı şu şekilde olmalıdır:
    {{
        "new_question": "Yeni oluşturduğun soru metni.",
        "options": [
            {{"option": "A", "text": "Şık metni"}},
            {{"option": "B", "text": "Şık metni"}},
            {{"option": "C", "text": "Şık metni"}},
            {{"option": "D", "text": "Şık metni"}},
            {{"option": "E", "text": "Şık metni"}}
        ],
        "correct_answer": "Doğru şıkkın harfi (A, B, C, D veya E)."
    }}

    Orijinal Soru ve Şıkları:
    {original_question_text}
    """

    try:
        response = LLM_MODEL.generate_content(prompt)
        cleaned_response_text = clean_gemini_response(response.text)
        
        return json.loads(cleaned_response_text)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Problematic response from LLM:\n{response.text}")
        return None
    except Exception as e:
        print(f"Error generating new question with LLM: {e}")
        return None

def main():
    """
    Main function to process a directory and generate new questions.
    """
    questions_folder = os.path.expanduser('~/Desktop/sorbi-sorular')
    output_folder = os.path.expanduser('~/Desktop/sorbi-yeni-sorular')
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        filenames = sorted(os.listdir(questions_folder))
    except FileNotFoundError:
        print(f"Error: Directory not found at '{questions_folder}'.")
        return

    for filename in filenames:
        file_path = os.path.join(questions_folder, filename)
        
        if not os.path.isfile(file_path) or filename.startswith('.'):
            continue

        file_extension = os.path.splitext(filename)[1].lower()
        
        original_question_text = ""
        original_image_bytes = None

        print(f"\n--- Processing file: {filename} to generate a new question ---")

        try:
            if file_extension in ['.png', '.jpg', '.jpeg']:
                with open(file_path, 'rb') as f:
                    original_image_bytes = f.read()
                
                new_question_data = generate_similar_question(
                    original_question_text="",
                    original_image_bytes=original_image_bytes
                )
            elif file_extension in ['.txt']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_question_text = f.read().strip()
                
                new_question_data = generate_similar_question(original_question_text=original_question_text)
            else:
                print(f"Warning: Skipping unsupported file type: {filename}")
                continue

            if new_question_data:
                output_filename = f"new_{os.path.splitext(filename)[0]}.txt"
                output_filepath = os.path.join(output_folder, output_filename)
                
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.write("Soru: " + new_question_data["new_question"] + "\n\n")
                    for opt in new_question_data["options"]:
                        f.write(f"{opt['option']}) {opt['text']}\n")
                    f.write(f"\nDoğru Cevap: {new_question_data['correct_answer']}\n")
                
                print(f"Successfully generated and saved: {output_filename}")
            else:
                print(f"Failed to generate a new question for {filename}.")
        
        except Exception as e:
            print(f"Error processing '{filename}': {e}")


if __name__ == "__main__":
    main()