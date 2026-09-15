import base64
from io import BytesIO

import requests
from PIL import Image as PILImage
import flet as ft

from app.views.base_view import BaseView
from app.views.mixins import AppBarMixin
from app.views.images_view import ImagesView


class HomeView(BaseView, AppBarMixin):
    """
    Главная страница приложения.
    """

    ROUTE = "/"

    def __init__(self, page: ft.Page):
        """
        Инициализирует главную страницу.

        :param page: Экземпляр страницы Flet.
        """

        super().__init__(page)
        self._img_cache: dict[str, str] = {}
        self.assemble_page()

    # ---------------- helpers ----------------

    def _h1(self, text: str) -> ft.Text:
        return ft.Text(text, size=28, weight=ft.FontWeight.BOLD)

    def _h2(self, text: str) -> ft.Text:
        return ft.Text(text, size=20, weight=ft.FontWeight.W_700)

    def _para(self, text: str) -> ft.Text:
        return ft.Text(text, size=14)

    def _bullet(self, text: str) -> ft.Row:
        return ft.Row(
            [ft.Icon(ft.Icons.CIRCLE, size=6), ft.Text(text)],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _link_btn(self, label: str, url: str) -> ft.TextButton:
        return ft.TextButton(label, on_click=lambda e, url=url: self.page.launch_url(url))

    def _code(self, lines: list[str]) -> ft.Container:
        return ft.Container(
            content=ft.Column([ft.Text(l, size=13, selectable=True) for l in lines],
                              tight=True, spacing=2),
            bgcolor=ft.colors.with_opacity(0.06, ft.colors.ON_SURFACE),
            border_radius=8,
            padding=12,
        )

    def _kv_link(self, label: str, url: str, tail: str = "") -> ft.Row:
        parts = [ft.Text(label + " ", weight=ft.FontWeight.BOLD), self._link_btn(url, url)]
        if tail:
            parts.append(ft.Text(f" — {tail}"))
        return ft.Row(parts, spacing=6, wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def _img_from_url(self, url: str, height: int = 500) -> ft.Control:
        try:
            if url not in self._img_cache:
                resp = requests.get(url, timeout=20)
                resp.raise_for_status()
                pil_img = PILImage.open(BytesIO(resp.content))
                if pil_img.mode not in ("RGB", "RGBA"):
                    pil_img = pil_img.convert("RGBA" if "A" in pil_img.getbands() else "RGB")
                buf = BytesIO()
                pil_img.save(buf, format="PNG", optimize=True)
                self._img_cache[url] = base64.b64encode(buf.getvalue()).decode("ascii")

            return ft.Image(src_base64=self._img_cache[url], fit=ft.ImageFit.CONTAIN, height=height)

        except Exception as ex:
            return ft.Column(
                [
                    ft.Row(
                        [ft.Icon(ft.Icons.BROKEN_IMAGE_OUTLINED), ft.Text("Failed to load image")],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Text(str(ex), size=12, color=ft.colors.ERROR),
                    ft.TextButton("Open image in browser", on_click=lambda e, u=url: self.page.launch_url(u)),
                ],
                spacing=6,
            )

    # --------- project structure (recursive tree) ---------

    def _tree_node(self, node: dict | str, level: int = 0) -> ft.Control:
        """
        node:
          - str: имя файла или подписи (без детей)
          - dict: { "name": "backend/", "link": "...", "children": [ ... ] }
        """
        left_pad = 16 * level

        if isinstance(node, str):
            return ft.Container(
                content=ft.ListTile(
                    dense=True,
                    title=ft.Text(node),
                    leading=ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED, size=16),
                ),
                padding=ft.padding.only(left=left_pad + 8),
            )

        name = node.get("name", "")
        link = node.get("link")
        children = node.get("children", [])

        if link:
            title_row = ft.Row(
                [
                    ft.Icon(ft.Icons.FOLDER, size=16),
                    self._link_btn(name, link),
                    ft.Text(node.get("suffix", "")),
                ],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        else:
            title_row = ft.Row(
                [ft.Icon(ft.Icons.FOLDER, size=16), ft.Text(name)],
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

        return ft.Container(
            content=ft.ExpansionTile(
                title=title_row,
                initially_expanded=node.get("expanded", False),
                controls=[self._tree_node(ch, level + 1) for ch in children],
            ),
            padding=ft.padding.only(left=left_pad),
        )

    def _project_structure_tree(self) -> ft.Control:
        root = {
            "name": "natural-language-image-search/",
            "expanded": True,
            "children": [
                ".env.dev — Development environment variables",
                "docker-compose.yml — Docker services configuration",
                "nginx.conf — NGINX reverse proxy configuration",
                {
                    "name": "backend/ ",
                    "suffix": "— Backend",
                    "link": "https://github.com/GrishaTS/natural-language-image-search/tree/main/backend",
                    "children": [
                        ".dockerignore",
                        "Dockerfile",
                        "requirements.txt",
                        {
                            "name": "app/",
                            "children": [
                                "main.py",
                                "config.py",
                                "models.py",
                                "router.py",
                                "schemas.py",
                                {"name": "api/", "children": ["__init__.py", "ml_api.py"]},
                                {
                                    "name": "database/",
                                    "children": [
                                        "__init__.py",
                                        "minio_client.py",
                                        "postgres_client.py",
                                        "qdrant_client.py",
                                        "test_data.py",
                                    ],
                                },
                                {
                                    "name": "repository/",
                                    "children": [
                                        "__init__.py",
                                        "base_repository.py",
                                        "postgres_repository.py",
                                        "minio_repository.py",
                                        "qdrant_repository.py",
                                        "repository.py",
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "frontend/ ",
                    "suffix": "— User Interface",
                    "link": "https://github.com/GrishaTS/natural-language-image-search/tree/main/frontend",
                    "children": [
                        ".dockerignore",
                        "Dockerfile",
                        "requirements.txt",
                        {
                            "name": "app/",
                            "children": [
                                "main.py",
                                "config.py",
                                "routes.py",
                                {"name": "api/", "children": ["__init__.py", "images_api.py", "image_api.py"]},
                                {"name": "data/", "children": ["__init__.py", "image_data.py"]},
                                {
                                    "name": "views/",
                                    "children": [
                                        "__init__.py",
                                        "base_view.py",
                                        "home_view.py",
                                        "images_view.py",
                                        "image_view.py",
                                        "delete_images_view.py",
                                        "search_images_view.py",
                                        {"name": "mixins/", "children": ["__init__.py", "app_bar_mixin.py", "grid_mixin.py", "nav_bar_mixin.py"]},
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "name": "ml_api/ ",
                    "suffix": "— ML Service",
                    "link": "https://github.com/GrishaTS/natural-language-image-search/tree/main/ml_api",
                    "children": [
                        ".dockerignore",
                        "Dockerfile",
                        "requirements.txt",
                        {
                            "name": "app/",
                            "children": [
                                "main.py",
                                "config.py",
                                "router.py",
                                "schemas.py",
                                {"name": "sm_clip/", "children": ["__init__.py", "base_clip.py", "clip_vit_b_32.py"]},
                            ],
                        },
                    ],
                },
                {
                    "name": "clip_fine_tuning/ ",
                    "suffix": "— Model Fine-tuning",
                    "link": "https://github.com/GrishaTS/natural-language-image-search/tree/main/clip_fine_tuning",
                    "children": [
                        "pyproject.toml",
                        "requirements.txt",
                        {
                            "name": "dataset/",
                            "children": [
                                {"name": "src/", "children": ["database.py", "models.py", "repository.py", "ruclip_dataset.py"]},
                                "1. qwen25_test.ipynb",
                                "2. clip993.ipynb",
                                "clip.db",
                                "qwen_api_keys.json",
                            ],
                        },
                        {
                            "name": "models/",
                            "children": [
                                {"name": "fine-tuning/", "children": ["1. ruclip_clip993.ipynb"]},
                                "1. open_clip.ipynb",
                                "2. ruclip.ipynb",
                                "3. ruclip_tiny.ipynb",
                                "base_clip.py",
                            ],
                        },
                    ],
                },
            ],
        }

        return ft.Column([self._h2("Project Structure"), self._tree_node(root)], spacing=8)

    # ---------------- assemble ----------------

    def assemble_page(self) -> None:
        """
        Собирает компоненты главной страницы.
        """
        self.app_bar()

        header = ft.Row(
            [
                ft.ElevatedButton(
                    "Перейти к галерее",
                    icon=ft.Icons.PHOTO_LIBRARY_OUTLINED,
                    on_click=lambda e: self.page.go(ImagesView.ROUTE),
                )
            ]
        )

        about = ft.Column(
            [
                self._h2("About"),
                self._para("Natural Language Image Search is an offline-capable photo management system that integrates:"),
                self._bullet("A responsive multi-page UI built with Flet for browsing, searching, and deleting images"),
                self._bullet("A robust FastAPI-based backend with support for PostgreSQL, MinIO, and Qdrant"),
                self._bullet("A dedicated ML microservice using CLIP/ruCLIP to enable text-based image search"),
                self._bullet("A flexible fine-tuning module for image captions and custom CLIP models (Qwen-2.5)"),
                self._bullet("Fully containerized with Docker"),
            ],
            spacing=6,
        )

        arch = ft.Column(
            [
                self._h2("Architecture"),
                self._img_from_url("https://github.com/user-attachments/assets/4e70a845-1029-46fb-8342-096d2249f331"),
                self._img_from_url("https://github.com/user-attachments/assets/0602964c-3c33-4bbd-be99-9d1360518ddd"),
            ],
            spacing=12,
        )

        usage = ft.Column(
            [
                self._h2("Usage"),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Service", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("URL", weight=ft.FontWeight.BOLD)),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Frontend")),
                                ft.DataCell(self._link_btn("http://localhost", "http://localhost")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Backend")),
                                ft.DataCell(self._link_btn("http://localhost:8000/docs", "http://localhost:8000/docs")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("ML API")),
                                ft.DataCell(self._link_btn("http://localhost:7189/docs", "http://localhost:7189/docs")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("MinIO")),
                                ft.DataCell(self._link_btn("http://localhost:9001", "http://localhost:9001")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Qdrant")),
                                ft.DataCell(self._link_btn("http://localhost:6333/dashboard", "http://localhost:6333/dashboard")),
                            ]
                        ),
                    ],
                ),
            ],
            spacing=8,
        )
        
        author = ft.Column(
            [
                self._h2("Author"),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Field", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Value", weight=ft.FontWeight.BOLD)),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Name")),
                                ft.DataCell(ft.Text("Bezrukov Grigoriy")),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Mail")),
                                ft.DataCell(ft.Text("gabezrukov@edu.hse.ru", selectable=True)),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Telegram")),
                                ft.DataCell(ft.Text("https://t.me/bezGriga", selectable=True)),
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Project Supervisor")),
                                ft.DataCell(ft.Text("Akhmetov Vadim")),
                            ]
                        ),
                    ],
                ),
            ],
            spacing=8,
        )

        body = ft.Container(
            padding=20,
            expand=True,
            content=ft.Column(
                [
                    header,
                    ft.Divider(),
                    about,
                    ft.Divider(),
                    arch,
                    ft.Divider(),
                    usage,
                    ft.Divider(),
                    self._project_structure_tree(),
                    ft.Divider(),
                    author
                ],
                spacing=14,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self.controls = [body]
