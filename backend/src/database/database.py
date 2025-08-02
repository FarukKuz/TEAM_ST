# exam-assistant-app/backend/src/database/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Base sınıfı, tüm veritabanı modellerinin miras alacağı temel sınıftır.
Base = declarative_base()

# Veritabanı URL'ini ortam değişkeninden güvenli bir şekilde alıyoruz.
# render'da "DATABASE_URL" adında bir ortam değişkeni oluşturduğun için bu kod doğru çalışacaktır.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """
    Tüm veritabanı tablolarını oluşturur.
    Base'den türetilen tüm modelleri import etmemiz gerekir.
    """
    from backend.src.database.models import (
        User,
        ExamType,
        Lesson,
        Topic,
        StudentTopicStatus,
        Question,
        AIAnswer,
        ForumAnswer,
        Follow,
        StudentInteraction,
    )
    # Base'den türeyen tüm modellerin metadata'sını kullanarak tabloları oluştur
    Base.metadata.create_all(bind=engine)