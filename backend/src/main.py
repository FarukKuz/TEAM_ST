# exam-assistant-app/backend/src/main.py
from dotenv import load_dotenv # Yeni eklenen satır
import os # Ortam değişkeni kontrolü için eklendi

# Ortam değişkenlerini, diğer import'lardan ve app tanımından önce yükle.
# Bu, tüm ayarların doğru bir şekilde okunmasını sağlar.
load_dotenv()

from fastapi import FastAPI
from backend.src.api.curriculum_routes import router as curriculum_router
from backend.src.database.database import create_db_and_tables

# Veritabanı URL'inin ayarlandığından emin ol
if not os.getenv("DATABASE_URL"):
    raise ValueError("DATABASE_URL ortam değişkeni ayarlanmamış!")

# **ÖNEMLİ:** Bu satır, veritabanı tablolarını oluşturmak içindir.
# Tablolarınız oluştuktan sonra bu satırı silebilir veya yorum satırı yapabilirsiniz.
create_db_and_tables()

app = FastAPI(
    title="Sınav Asistanı Backend API",
    description="Yapay zeka etiketleme, forum ve müfredat gibi sınav asistanı özelliklerini yöneten API.",
    version="1.0.0",
)

# API rotaları
app.include_router(curriculum_router, prefix="/api/curriculum", tags=["Müfredat ve Etiketleme"])
# Diğer rotalar buraya eklenecektir.

@app.get("/")
async def read_root():
    return {"mesaj": "Sınav Asistanı Backend API'sine hoş geldiniz!"}