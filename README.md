# Natural Language Image Search

Офлайн-галерея, в которой фотографии ищутся по текстовому описанию на русском — без ручных тегов и без подключения к интернету.

> Курсовой проект ВШЭ (ФКН, «Программная инженерия», 2025).

![Natural Language Image Search — галерея](https://github.com/user-attachments/assets/4eed90c5-67c1-4f4a-828c-f775d9a00106)
![Natural Language Image Search — поиск](https://github.com/user-attachments/assets/ac87ae18-68d4-41b7-a3f3-a3a00a3c2443)

## Что умеет

- Загружать, просматривать и удалять фотографии; хранить превью и метаданные.
- Искать по тексту: запрос превращается в эмбеддинг ruCLIP, ближайшие изображения находятся в Qdrant.
- Работать полностью локально: все сервисы в Docker, модель скачивается один раз.

## Модель

- Попробовал OpenCLIP, ruCLIP и ruCLIP-tiny — ноутбуки в [`clip_fine_tuning/models/`](clip_fine_tuning/models/).
- Собрал датасет **clip993**: 993 изображения с подписями на русском, подписи сгенерировал Qwen 2.5 через DashScope API ([`clip_fine_tuning/dataset/`](clip_fine_tuning/dataset/)).
- Дообучил ruCLIP на clip993. Веса — [bezGriga/ruclip-finetuned-clip993](https://huggingface.co/bezGriga/ruclip-finetuned-clip993) на Hugging Face.

![Дообучение ruCLIP на clip993](https://github.com/user-attachments/assets/fd750ddd-ff3a-4aa8-b590-cd266907baf1)

## Архитектура

![Архитектура Natural Language Image Search](https://github.com/user-attachments/assets/4e70a845-1029-46fb-8342-096d2249f331)
![Потоки загрузки и поиска](https://github.com/user-attachments/assets/0602964c-3c33-4bbd-be99-9d1360518ddd)

- **Frontend (Flet)** — галерея, просмотр, удаление, поиск.
- **Backend (FastAPI)** — REST API; метаданные в PostgreSQL, файлы и превью в MinIO, эмбеддинги в Qdrant.
- **ML API (FastAPI)** — эмбеддинги изображений и текста моделью ruCLIP.
- **nginx** — единая точка входа.

## Стек

- **ML:** PyTorch, ruCLIP, OpenCLIP, Hugging Face Hub, Qwen 2.5 (DashScope)
- **Backend:** Python, FastAPI, SQLAlchemy, asyncpg, Pydantic
- **Хранилища:** PostgreSQL, MinIO, Qdrant
- **UI:** Flet
- **Инфраструктура:** Docker Compose, nginx

## Запуск

```bash
git clone https://github.com/GrishaTS/natural-language-image-search
cd natural-language-image-search

# веса дообученного ruCLIP
pip install huggingface_hub==0.23.3 --force-reinstall --no-deps
huggingface-cli download bezGriga/ruclip-finetuned-clip993 ruclip_clip993.pt \
  --cache-dir ml_api/app/sm_clip/hugface/ruclip_clip993

docker compose --env-file .env.dev up --build
```

- Интерфейс: http://localhost
- Backend API: http://localhost:8000/docs
- ML API: http://localhost:7189/docs
- MinIO: http://localhost:9001 (логин и пароль — в `.env.dev`)
- Qdrant: http://localhost:6333/dashboard

Для генерации подписей своим датасетом положите ключи DashScope в `clip_fine_tuning/dataset/qwen_api_keys.json` (файл в `.gitignore`).

## Структура

```
frontend/          UI на Flet
backend/           FastAPI: загрузка, поиск, удаление; PostgreSQL, MinIO, Qdrant
ml_api/            сервис эмбеддингов (ruCLIP, CLIP ViT-B/32)
clip_fine_tuning/  датасет clip993 и дообучение ruCLIP
technical_docs/    документация курсового проекта
```

Подробное описание каждого сервиса — в README внутри папок.

## Лицензия

[MIT](LICENSE)
