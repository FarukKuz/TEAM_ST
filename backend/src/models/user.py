from sqlalchemy import Column, Integer, String, DateTime
from backend.src.core.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(255), unique=True, nullable=False)  
    email = Column(String(100), unique=True , nullable=False)
    username = Column(String(50), nullable=False)
    profile_picture = Column(String, default="")
    login_type = Column(String)  
    created_at = Column(DateTime, default=datetime.utcnow)
