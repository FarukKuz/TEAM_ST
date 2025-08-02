from sqlalchemy.orm import Session
from backend.src.models.user import User
from datetime import datetime


def get_user_by_uid(db: Session, uid: str):
    return db.query(User).filter(User.uid == uid).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):
    new_user = User(
        uid=user_data["uid"],
        email=user_data["email"],
        username=user_data["username"],
        profile_picture=user_data.get("profile_picture", ""),
        login_type=user_data["login_type"],
        created_at=datetime.utcnow
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
