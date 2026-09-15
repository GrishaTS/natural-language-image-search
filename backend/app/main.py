from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import (
    create_minio,
    create_postgres,
    create_qdrant,
    delete_minio,
    delete_postgres,
    delete_qdrant,
    fill_test_data,
)
from app.router import router_health, router_image, router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом приложения.

    В режиме DEV очищает базу данных и заполняет тестовыми данными.
    В обоих режимах создаёт необходимые сервисы.
    """
    if settings.APP_MODE == "DEV":
        await delete_postgres()
        await delete_minio()
        await delete_qdrant()
        print("База очищена")

    await create_postgres()
    await create_minio()
    await create_qdrant()
    print("База готова к работе")

    if settings.APP_MODE == "DEV":
        await fill_test_data()
        print("База заполнена тестовыми данными")

    yield
    print("Выключение")


print(f'Starting server on {settings.BACKEND_HOST}:{settings.BACKEND_PORT}')
app = FastAPI(title="Natural Language Image Search - backend", lifespan=lifespan)

# Регистрация роутеров
app.include_router(router_health)
app.include_router(router_image)
app.include_router(router_images)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
