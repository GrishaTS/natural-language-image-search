# Natural Language Image Search — Backend
![image](https://github.com/user-attachments/assets/d0e77c52-7e3e-4d01-887f-855c8411ab42)

___
## About
*Natural Language Image Search — Backend is the server-side component of the Natural Language Image Search project, a photo management system designed to work offline. The backend is built with FastAPI and integrates multiple services to handle image storage, search, and metadata management.*

Key features:
- Image upload and retrieval using RESTful APIs
- Search by text queries with the help of a machine learning microservice (CLIP-based)
- Storage of image metadata (e.g., path, preview, size, creation date, and embeddings)
- Integration with PostgreSQL, MinIO, and Qdrant for relational, object, and vector data respectively
- Environment support for development and production, with automated setup and test data generation in DEV mode
- The backend is containerized using Docker and is designed to interact seamlessly with the frontend and ML microservices.


___
## Project Structure

<details>
  <summary>📂 backend/</summary>
  <ul>
    <li>📄 <code>.dockerignore</code> — Files and folders to exclude from Docker build context</li>
    <li>📄 <code>Dockerfile</code> — Instructions to build the backend Docker image</li>
    <li>📄 <code>requirements.txt</code> — Python dependencies for the backend</li>
    <details>
      <summary>📂 app/</summary>
      <ul>
        <li>📄 <code>main.py</code> — FastAPI application entry point</li>
        <li>📄 <code>config.py</code> — Application settings and configuration</li>
        <li>📄 <code>models.py</code> — SQLAlchemy models and database schemas</li>
        <li>📄 <code>router.py</code> — API router combining all endpoints</li>
        <li>📄 <code>schemas.py</code> — Pydantic models for request and response validation</li>
        <details>
          <summary>📂 api/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the API module</li>
            <li>📄 <code>ml_api.py</code> — Routes for interacting with the ML microservice</li>
          </ul>
        </details>
        <details>
          <summary>📂 database/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the database module</li>
            <li>📄 <code>minio_client.py</code> — Client setup for MinIO object storage</li>
            <li>📄 <code>postgres_client.py</code> — Client setup for PostgreSQL database</li>
            <li>📄 <code>qdrant_client.py</code> — Client setup for Qdrant vector database</li>
            <li>📄 <code>test_data.py</code> — Test data and helper functions for development</li>
          </ul>
        </details>
        <details>
          <summary>📂 repository/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the repository module</li>
            <li>📄 <code>base_repository.py</code> — Abstract base class for all repositories</li>
            <li>📄 <code>postgres_repository.py</code> — PostgreSQL-specific database operations</li>
            <li>📄 <code>minio_repository.py</code> — MinIO-specific storage operations</li>
            <li>📄 <code>qdrant_repository.py</code> — Qdrant-specific vector operations</li>
            <li>📄 <code>repository.py</code> — Aggregated interface for using all repositories</li>
          </ul>
        </details>
      </ul>
    </details>
  </ul>
</details>

___
## Technologies Used
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi) ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-333333?logo=uvicorn) ![Pydantic](https://img.shields.io/badge/Pydantic-Validation-4B8BBE?logo=pydantic) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-000000?logo=sqlalchemy) ![Pydantic Settings](https://img.shields.io/badge/Settings-Config-4B8BBE) ![Multipart](https://img.shields.io/badge/Multipart-Uploads-FFD43B) ![Pillow](https://img.shields.io/badge/Images-Pillow-316192?logo=python) ![Aiofiles](https://img.shields.io/badge/Async-FileIO-6A5ACD) ![Asyncpg](https://img.shields.io/badge/PostgreSQL-Asyncpg-00599C) ![HTTPX](https://img.shields.io/badge/HTTP-Client-0E8AC8) ![NumPy](https://img.shields.io/badge/Array-Numerics-013243?logo=numpy) ![MinIO](https://img.shields.io/badge/ObjectStorage-MinIO-F05032?logo=minio) ![Qdrant](https://img.shields.io/badge/VectorDB-Qdrant-FF6F00) ![Requests](https://img.shields.io/badge/Requests-SyncClient-20232A?logo=python)
