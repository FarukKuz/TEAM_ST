from dotenv import load_dotenv
import os
import logging
from fastapi import FastAPI, HTTPException

# !!!!!! Render'a kök dizin olarak backend girdiğimiz için düzenledik. Local'de çalıştırırken düzeltilmeli!!!!!!
from backend.src.api.curriculum_routes import router as curriculum_router
from backend.src.database.database import create_db_and_tables, verify_tables, test_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sınav Asistanı Backend API",
    description="Yapay zeka etiketleme, forum ve müfredat gibi sınav asistanı özelliklerini yöneten API.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Uygulama başlatılıyor...")
    
    if test_connection():
        logger.info("Veritabanı bağlantısı başarılı")
    else:
        logger.error("Veritabanı bağlantısı başarısız!")
        return
    
    success = create_db_and_tables()
    if success:
        logger.info("Tablo oluşturma işlemi tamamlandı")
        verify_tables()
    else:
        logger.error("Tablo oluşturma işlemi başarısız!")

app.include_router(curriculum_router, prefix="/api/curriculum", tags=["Müfredat ve Etiketleme"])

@app.get("/")
async def read_root():
    return {"mesaj": "Sınav Asistanı Backend API'sine hoş geldiniz!"}


# ===== DEBUG VE SAĞLIK KONTROL ENDPOINT'LERİ =====
# Bu endpoint'ler geliştirme ve debug için eklenmiştir
@app.get("/health")
async def health_check():
    try:
        # Veritabanı bağlantısını test et
        db_status = test_connection()
        
        # Tabloları kontrol et
        tables = verify_tables()
        
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database_connection": db_status,
            "tables_count": len(tables),
            "tables": tables,
            "message": "Sınav Asistanı Backend API çalışıyor"
        }
    except Exception as e:
        logger.error(f"Health check hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/tables")
async def debug_tables():
    """Debug için tablo bilgilerini döndür"""
    try:
        tables = verify_tables()
        return {
            "tables_found": len(tables),
            "table_names": tables,
            "status": "success" if tables else "no_tables_found",
            "expected_tables": [
                'users', 'exam_types', 'lessons', 'topics', 
                'student_topic_statuses', 'questions', 'ai_answers', 
                'forum_answers', 'follows', 'student_interactions'
            ]
        }
    except Exception as e:
        logger.error(f"Debug tables hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/recreate-tables")
async def recreate_tables():
    """
    Tabloları yeniden oluştur (sadece geliştirme için)
    UYARI: Bu endpoint production'da dikkatli kullanılmalıdır
    """
    try:
        logger.info("Tablolar yeniden oluşturuluyor...")
        success = create_db_and_tables()
        
        if success:
            tables = verify_tables()
            return {
                "status": "success",
                "message": "Tablolar başarıyla oluşturuldu",
                "tables_created": len(tables),
                "tables": tables
            }
        else:
            return {
                "status": "error",
                "message": "Tablo oluşturma başarısız"
            }
    except Exception as e:
        logger.error(f"Tablo yeniden oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))