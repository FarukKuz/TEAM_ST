import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Enum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base sınıfı, tüm veritabanı modellerinin miras alacağı temel sınıftır.
Base = declarative_base()

# Kullanıcı etkileşim tiplerini tanımlayan Enum sınıfı
class InteractionType(enum.Enum):
    ask = "ask"
    answer = "answer"
    ai_use = "ai_use"

# Kullanıcıların temel bilgilerini içeren tablo
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    google_uid = Column(String, unique=True, nullable=True)
    profile_picture = Column(Text, nullable=True)
    points = Column(Integer, default=5, nullable=False)
    login_type = Column(Enum('google', 'email', name='login_type_enum'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişkiler:
    questions = relationship("Question", back_populates="user")
    forum_answers = relationship("ForumAnswer", back_populates="user")
    student_topic_status = relationship("StudentTopicStatus", back_populates="user")
    student_interactions = relationship("StudentInteraction", back_populates="user")
    following = relationship("Follow", foreign_keys='Follow.following_user_id', back_populates="following_user")
    followers = relationship("Follow", foreign_keys='Follow.followed_user_id', back_populates="followed_user")

# Sınav tiplerini tanımlayan tablo (TYT, KPSS gibi)
class ExamType(Base):
    __tablename__ = "exam_type"

    exam_type_id = Column(Integer, primary_key=True)
    exam_name = Column(String, nullable=False)

    # İlişkiler:
    lessons = relationship("Lesson", back_populates="exam_type")

# Sınavlara ait dersleri tanımlayan tablo
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    exam_type_id = Column(Integer, ForeignKey("exam_type.exam_type_id"), nullable=False)

    # İlişkiler:
    exam_type = relationship("ExamType", back_populates="lessons")
    topics = relationship("Topic", back_populates="lesson")
    questions = relationship("Question", back_populates="lesson")

# Derslere ait konuları tanımlayan tablo
class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    name = Column(String, nullable=False)

    # İlişkiler:
    lesson = relationship("Lesson", back_populates="topics")
    student_topic_status = relationship("StudentTopicStatus", back_populates="topic")
    student_interactions = relationship("StudentInteraction", back_populates="topic")
    questions = relationship("Question", back_populates="topic")

# Öğrencilerin konu bazlı ilerlemesini ve durumunu takip eden tablo
class StudentTopicStatus(Base):
    __tablename__ = "student_topic_status"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    is_known = Column(Boolean, default=False, nullable=False)
    progress_level = Column(Integer, default=5, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # İlişkiler:
    user = relationship("User", back_populates="student_topic_status")
    topic = relationship("Topic", back_populates="student_topic_status")

# Kullanıcılar tarafından sorulan soruları içeren ana tablo
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_text = Column(Text, nullable=True)
    image_url = Column(String, nullable=True) # Diyagramda yoktu, ancak önceki görüşmelerimize dayanarak ekledim
    exam_type = Column(String, nullable=True) # Diyagramda varchar, bu modelin AI tarafından etiketlenen sınav tipini saklamasına izin verir
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    is_forum_post = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişkiler:
    user = relationship("User", back_populates="questions")
    lesson = relationship("Lesson", back_populates="questions")
    topic = relationship("Topic", back_populates="questions")
    ai_answers = relationship("AIAnswer", back_populates="question")
    forum_answers = relationship("ForumAnswer", back_populates="question")

# Yapay zeka tarafından verilen yanıtları içeren tablo
class AIAnswer(Base):
    __tablename__ = "ai_answers"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişkiler:
    question = relationship("Question", back_populates="ai_answers")

# Forum sorularına kullanıcılar tarafından verilen yanıtları içeren tablo
class ForumAnswer(Base):
    __tablename__ = "forum_answers"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    is_accepted = Column(Boolean, default=False, nullable=False)
    upvotes = Column(Integer, default=0, nullable=False)
    downvotes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişkiler:
    question = relationship("Question", back_populates="forum_answers")
    user = relationship("User", back_populates="forum_answers")

# Kullanıcıların birbirlerini takip etmesini sağlayan ilişki tablosu
class Follow(Base):
    __tablename__ = "follows"

    following_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    followed_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # İlişkiler:
    following_user = relationship("User", foreign_keys=[following_user_id], back_populates="following")
    followed_user = relationship("User", foreign_keys=[followed_user_id], back_populates="followers")

# Öğrencinin konu bazlı etkileşimlerini (soru sorma, cevaplama, AI kullanma) loglayan tablo
class StudentInteraction(Base):
    __tablename__ = "student_interactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    interaction_type = Column(Enum(InteractionType), nullable=False)
    interaction_time = Column(DateTime, default=datetime.utcnow)

    # İlişkiler:
    user = relationship("User", back_populates="student_interactions")
    topic = relationship("Topic", back_populates="student_interactions")