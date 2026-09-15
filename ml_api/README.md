# Natural Language Image Search — ML Api
![image](https://github.com/user-attachments/assets/daa4de53-04fd-4726-8ad8-02144d0c8279)

___
## About
*Natural Language Image Search — ML Api is the machine learning microservice of the Natural Language Image Search project. It is responsible for generating image and text embeddings. The service is built with FastAPI and is designed to integrate seamlessly with other components of the system.*

Key features:
- Generation of embeddings for both images and text  
- Asynchronous service using FastAPI and Uvicorn  

___
## Project Structure

<details>
  <summary>📂 ml_api/</summary>
  <ul>
    <li>📄 <code>.dockerignore</code> — Files and folders excluded from Docker build context</li>
    <li>📄 <code>Dockerfile</code> — Instructions for building the ML service Docker image</li>
    <li>📄 <code>requirements.txt</code> — Python dependencies for the ML microservice</li>
    <details>
      <summary>📂 app/</summary>
      <ul>
        <li>📄 <code>main.py</code> — Entry point of the FastAPI ML service</li>
        <li>📄 <code>config.py</code> — Configuration for model and app settings</li>
        <li>📄 <code>router.py</code> — API routes for text-to-image search and embeddings</li>
        <li>📄 <code>schemas.py</code> — Pydantic models for request/response validation</li>
        <details>
          <summary>📂 sm_clip/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the sm_clip module</li>
            <li>📄 <code>base_clip.py</code> — Abstract base class for CLIP models</li>
            <li>📄 <code>clip_vit_b_32.py</code> — CLIP ViT-B/32 model wrapper implementation</li>
            <li>📄 <code>ruclip_clip993.py</code> — RuClip finetuned on clip993</li>
          </ul>
        </details>
      </ul>
    </details>
  </ul>
</details>

___
## Technologies Used
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)   ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-333333?logo=uvicorn)   ![Pydantic](https://img.shields.io/badge/Pydantic-Validation-4B8BBE?logo=pydantic)   ![Pillow](https://img.shields.io/badge/Images-Pillow-316192)   ![NumPy](https://img.shields.io/badge/Numerics-NumPy-013243?logo=numpy)   ![Hugging Face](https://img.shields.io/badge/ModelHub-HuggingFace-FF4C7B?logo=huggingface)   ![Requests](https://img.shields.io/badge/HTTP-Requests-20232A)   ![Python-Multipart](https://img.shields.io/badge/Uploads-Multipart-FFD43B)   ![Aiofiles](https://img.shields.io/badge/Async-FileIO-6A5ACD)   ![RuCLIP](https://img.shields.io/badge/Model-RuCLIP-orange)   ![YouTokenToMe](https://img.shields.io/badge/Tokenizer-YouTokenToMe-blue)   ![Cython](https://img.shields.io/badge/Cython-Accelerated-FF6600)
