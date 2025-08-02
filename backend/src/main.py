# exam-assistant-app/backend/src/main.py
from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
# !!!!!! Render'a kök dizin olarak backend girdiğimiz için düzenledik. Local'de çalıştırırken düzeltilmeli!!!!!!
from src.api.curriculum_routes import router as curriculum_router
from src.database.database import create_db_and_tables

if not os.getenv("DATABASE_URL"):
    raise ValueError("DATABASE_URL ortam değişkeni ayarlanmamış!")

create_db_and_tables()

app = FastAPI(
    title="Sınav Asistanı Backend API",
    description="Yapay zeka etiketleme, forum ve müfredat gibi sınav asistanı özelliklerini yöneten API.",
    version="1.0.0",
)

# API rotaları
app.include_router(curriculum_router, prefix="/api/curriculum", tags=["Müfredat ve Etiketleme"])

@app.get("/")
async def read_root():
    return {"mesaj": "Sınav Asistanı Backend API'sine hoş geldiniz!"}