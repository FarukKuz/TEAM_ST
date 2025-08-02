from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.src.dependencies.auth import get_current_user
from backend.src.core.database import SessionLocal
from backend.src.services.auth_service import get_user_by_uid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me")
def get_me(user_data=Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_uid(db, user_data["uid"])
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    return {
        "uid": user.uid,
        "email": user.email,
        "username": user.username,
        "profile_picture": user.profile_picture,
        "login_type": user.login_type,
        "created_at": user.created_at
    }
