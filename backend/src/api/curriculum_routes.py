from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.src.services.curriculum_service import CurriculumService
from ai_core.config import EXAM_DATA_FILEPATHS


class TagQuestionRequest(BaseModel):
    question_text: str
    exam_type: str

class TagQuestionResponse(BaseModel):
    course: str
    topic: str
    error: str | None = None

router = APIRouter()
curriculum_service = CurriculumService()

@router.post("/tag_question", response_model=TagQuestionResponse)
async def tag_question_endpoint(request: TagQuestionRequest):

    # Gelen sınav tipinin config'de tanımlı olup olmadığını kontrol et
    if request.exam_type.upper() not in EXAM_DATA_FILEPATHS:
        raise HTTPException(status_code=400, detail=f"Geçersiz sınav tipi: '{request.exam_type}'. Desteklenenler: {list(EXAM_DATA_FILEPATHS.keys())}")

    result = curriculum_service.get_question_tags(request.question_text, request.exam_type)

    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return TagQuestionResponse(**result)