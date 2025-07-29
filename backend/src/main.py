from fastapi import FastAPI
from backend.src.api.curriculum_routes import router as curriculum_router # Router'ı import ediyoruz

app = FastAPI(
    title="Sınav Asistanı Backend API",
    description="Yapay zeka etiketleme, forum ve müfredat gibi sınav asistanı özelliklerini yöneten API.",
    version="1.0.0",
)

# API rotaları
app.include_router(curriculum_router, prefix="/api/curriculum", tags=["Müfredat ve Etiketleme"])
# Diğer rotalar (auth_routes, users_routes, forum_routes, ai_assistant_routes) buraya eklenecektir.

@app.get("/")
async def read_root():
    return {"mesaj": "Sınav Asistanı Backend API'sine hoş geldiniz!"}
