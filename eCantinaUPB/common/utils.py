from pathlib import Path
from io import BytesIO
import os
import sys
import requests
import gradio as gr
from PIL import Image
from common.options import opts


def ensure_dirs():
    Path(opts["storage_img_path"]).mkdir(parents=True, exist_ok=True)
    Path(opts["storage_model_path"]).mkdir(parents=True, exist_ok=True)


def fetch_image(url: str) -> Image:
    try:
        response = requests.get(url)
    except Exception as e:
        gr.Warning(e)
        return None

    if response.status_code == 200:
        img_data = response.content
        result = Image.open(BytesIO(img_data))
        return result
    if response.status_code == 301:
        return fetch_image(response.headers["Location"])

    gr.Warning(f"HTTP status code: {response.status_code}")
    return None


def create_tag(tag_name: str) -> None:
    (Path(opts["storage_img_path"]) / tag_name).mkdir(parents=True, exist_ok=True)


def get_training_tags() -> list:
    return [
        p.name
        for p in Path(opts["storage_img_path"]).glob("**/")
        if p.is_dir() and p.name != Path(opts["storage_img_path"]).name
    ]


def get_image_paths_for_training_tag(tag: str) -> list:
    return [
        path
        for path in (Path(opts["storage_img_path"]) / tag).glob(
            f"*.{opts['storage_img_fmt']}"
        )
    ]


def get_image_paths_for_training_tags(tags: list) -> list:
    return [path for tag in tags for path in get_image_paths_for_training_tag(tag)]


def get_lookup_paths() -> list:
    paths: list = [opts["storage_model_path"]]
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        paths.append(str(Path(sys._MEIPASS) / "models"))
    return paths


def get_model_paths() -> list:
    return [
        file
        for dir_path in get_lookup_paths()
        for file in Path(dir_path).glob("**/*.npz")
    ]
