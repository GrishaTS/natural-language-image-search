import ruclip
import torch
import numpy as np
from huggingface_hub import hf_hub_download
from PIL import Image

from app.sm_clip.base_clip import BaseClip

class RuClipFTClip933(BaseClip):
    """
    Дообученная RuClip модель на clip993  
    https://github.com/GrishaTS/natural-language-image-search/blob/main/clip_fine_tuning/models/fine-tuning/1.%20ruclip_clip993.ipynb
    """

    MODEL_NAME = "ruclip_clip993"
    CHECKPOINT = hf_hub_download(
        repo_id="bezGriga/ruclip-finetuned-clip993",
        filename="ruclip_clip993.pt",
        cache_dir="app/sm_clip/hugface/ruclip_clip993"
    )

    def __init__(self):
        """
        Инициализирует модель CLIP ViT-B-32.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print('Model loading...')
        self.model, self.processor = ruclip.load('ruclip-vit-base-patch32-384', device=self.device)
        state_dict = torch.load(self.CHECKPOINT, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.eval()
        print('Model loaded successfully.')

    async def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Получает эмбеддинг изображения.

        :param image: Изображение в формате PIL.Image.
        :return: Векторное представление изображения в виде np.ndarray.
        """
        image = image.convert("RGB")
        inputs = self.processor(images=[image])
        pixel_values = inputs["pixel_values"].to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(pixel_values)
            image_features /= image_features.norm(dim=-1, keepdim=True)

        return image_features.cpu().numpy()[0]

    async def get_text_embedding(self, text: str) -> np.ndarray:
        """
        Получает эмбеддинг текста.

        :param text: Входной текст.
        :return: Векторное представление текста в виде np.ndarray.
        """
        inputs = self.processor(text=[text])
        input_ids = inputs["input_ids"].to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(input_ids)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features.cpu().numpy()[0]
