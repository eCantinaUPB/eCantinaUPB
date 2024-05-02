from pathlib import Path
import secrets
import logging
import gradio as gr
import numpy as np
from PIL import Image
from common.options import opts
from common.utils import get_training_tags, get_image_paths_for_training_tag


class Identifier:
    class Masks:
        @staticmethod
        def circle(size: int) -> np.array:
            mask = np.zeros((size, size), dtype=np.float32)
            for i in range(size):
                for j in range(size):
                    x, y = np.abs(i - size // 2), np.abs(j - size // 2)
                    distance = np.sqrt(x**2 + y**2)
                    if distance <= size // 2:
                        mask[i, j] = 1.0
            return np.tile(mask[:, :, np.newaxis], (1, 1, 3))

        @staticmethod
        def empty(size: int) -> np.array:
            return np.ones((size, size, 3), dtype=np.float32)

    @staticmethod
    def train(model_name: str, model_res: int) -> dict:
        weights: dict = {}

        tags: list = get_training_tags()

        if not tags:
            gr.Warning("Nu exista etichete")
            return

        for tag in tags:
            gr.Info(f"Se antreneaza modelul pentru clasa {tag}")

            training_images = [
                Identifier.process_image(Image.open(path), model_res)
                for path in get_image_paths_for_training_tag(tag)
            ]

            if not training_images:
                gr.Warning(f"Nu exista imagini cu eticheta {tag}, se omite")
                continue

            weights[tag] = np.mean(np.stack(training_images, axis=0), axis=0)

        if model_name:
            model_path = Path(opts["storage_model_path"]) / model_name
        else:
            model_path = Path(opts["storage_model_path"]) / secrets.token_urlsafe(8)

        Identifier.save_to_file(weights, model_path)
        gr.Info(f"Modelul a fost salvat ca {str(model_path)}.npz")

    @staticmethod
    def process_image(image: Image, res: int) -> np.array:
        return (
            np.array(
                image.convert("RGB").resize((res, res)),
                dtype=np.float32,
            )
            / 255.0
        )

    @staticmethod
    def interrogate(model_weights: dict, image: Image, mask) -> dict:
        results: dict = {}

        model_res = next(iter(model_weights.values())).shape[0]
        target = Identifier.process_image(image, model_res)

        mask_weights = mask(model_res)

        for class_name, weights in model_weights.items():
            difference = (weights - target) * mask_weights
            mask_size = np.sum(mask_weights)
            results[class_name] = float(
                1.0 - (abs(float(np.sum(difference))) / mask_size / 3.0)
            )
        return results

    @staticmethod
    def save_to_file(weights: dict, path: Path) -> None:
        np.savez(path, **weights)

    @staticmethod
    def load_from_file(path: Path) -> dict:
        loaded_data = np.load(path)
        return {class_name: loaded_data[class_name] for class_name in loaded_data.files}

    current_model: dict = {}
