import os
import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# SSL yüzünden çok hata aldık!
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"}  # SSL zorunlu
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"Veritabanı bağlantısı başarılı: {version}")
            return True
    except Exception as e:
        logger.error(f"Veritabanı bağlantı hatası: {e}")
        return False

def list_existing_tables():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Mevcut tablolar: {tables}")
        return tables
    except Exception as e:
        logger.error(f"Tablo listeleme hatası: {e}")
        return []

def create_db_and_tables():
    try:
        if not test_connection():
            raise Exception("Veritabanı bağlantısı kurulamadı")
        
        logger.info("Mevcut tablolar kontrol ediliyor...")
        existing_tables = list_existing_tables()
        
        logger.info("Modeller import ediliyor...")
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
        
        logger.info("Tablolar oluşturuluyor...")
        Base.metadata.create_all(bind=engine)
        
        logger.info("Tablo oluşturma tamamlandı, kontrol ediliyor...")
        new_tables = list_existing_tables()
        
        created_tables = set(new_tables) - set(existing_tables)
        if created_tables:
            logger.info(f"Yeni oluşturulan tablolar: {created_tables}")
        else:
            logger.info("Tüm tablolar zaten mevcut veya hiç tablo oluşturulmadı")
        
        expected_tables = [
            'users', 'exam_types', 'lessons', 'topics', 
            'student_topic_statuses', 'questions', 'ai_answers', 
            'forum_answers', 'follows', 'student_interactions'
        ]
        
        missing_tables = []
        for table in expected_tables:
            if table not in new_tables:
                missing_tables.append(table)
        
        if missing_tables:
            logger.warning(f"Eksik tablolar: {missing_tables}")
        else:
            logger.info("Tüm beklenen tablolar mevcut!")
            
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy hatası: {e}")
        return False
    except ImportError as e:
        logger.error(f"Model import hatası: {e}")
        return False
    except Exception as e:
        logger.error(f"Genel hata: {e}")
        return False

def verify_tables():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        logger.info(f"Toplam {len(tables)} tablo bulundu:")
        for table in tables:
            columns = inspector.get_columns(table)
            logger.info(f"  {table}: {len(columns)} sütun")
            for col in columns:
                logger.info(f"    - {col['name']} ({col['type']})")
        
        return tables
    except Exception as e:
        logger.error(f"Tablo doğrulama hatası: {e}")
        return []