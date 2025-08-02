from fastapi import FastAPI
from backend.src.api.curriculum_routes import router as curriculum_router # Router'ı import ediyoruz
from backend.src.api.auth_routes import router as auth_router 
from backend.src.api.users_routes import router as users_router

app = FastAPI(
    title="Sınav Asistanı Backend API",
    description="Yapay zeka etiketleme, forum ve müfredat gibi sınav asistanı özelliklerini yöneten API.",
    version="1.0.0",
)

# API rotaları
app.include_router(curriculum_router, prefix="/api/curriculum", tags=["Müfredat ve Etiketleme"])
app.include_router(auth_router, prefix="/api/auth", tags=["Kimlik Doğrulama"]) 

app.include_router(users_router, prefix="/api/users", tags=["Kullanıcı"])
# Diğer rotalar (auth_routes, users_routes, forum_routes, ai_assistant_routes) buraya eklenecektir.

@app.get("/")
async def read_root():
    return {"mesaj": "Sınav Asistanı Backend API'sine hoş geldiniz!"}
