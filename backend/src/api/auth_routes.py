from fastapi import APIRouter, HTTPException, status
from backend.src.services.auth_service import get_user_by_uid, get_user_by_email, create_user
from backend.src.core.database import SessionLocal
from backend.src.schemas.auth_schemas import UserIn, UserUID

router = APIRouter()

@router.post("/register")
def register(user: UserIn):
    db = SessionLocal()
    try:
        if get_user_by_uid(db, user.uid) or get_user_by_email(db, user.email):
            raise HTTPException(status_code=409, detail="Bu e-posta veya UID zaten kayıtlı.")
        created = create_user(db, user.dict())
        return {
            "status": "success",
            "message": "Kayıt başarılı.",
            "user": {
                "username": created.username,
                "email": created.email
            }
        }
    finally:
        db.close()

@router.post("/login")
def login(user: UserUID):
    db = SessionLocal()
    try:
        existing_user = get_user_by_uid(db, user.uid)
        if existing_user:
            return {
                "status": "success",
                "message": "Giriş başarılı.",
                "user": {
                    "username": existing_user.username,
                    "email": existing_user.email
                }
            }
        else:
            raise HTTPException(status_code=404, detail="Kayıt bulunamadı. Lütfen kayıt olun.")
    finally:
        db.close()
