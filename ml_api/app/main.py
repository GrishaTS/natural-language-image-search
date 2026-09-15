from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import router_health, router_embed
from app.config import settings

print(f'Starting server on {settings.ML_API_HOST}:{settings.ML_API_PORT}')
# Создание экземпляра FastAPI
app = FastAPI(title="Natural Language Image Search - ml-api")

# Подключение маршрутов
app.include_router(router_health)
app.include_router(router_embed)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BACKEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
