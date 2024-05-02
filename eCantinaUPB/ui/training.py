import secrets
from pathlib import Path
from PIL import Image
import gradio as gr
from ir import Identifier
from common.utils import (
    get_training_tags,
    get_image_paths_for_training_tags,
    create_tag,
    fetch_image,
)
from common.options import opts


def apply_tag(image, tag_names):
    if not image:
        gr.Warning("Introduceti o imagine")
        return
    saved_image = (
        image["background"]
        .convert("RGB")
        .resize((opts["storage_img_res"], opts["storage_img_res"]))
    )
    filename: str = f"{secrets.token_urlsafe(16)}.{opts['storage_img_fmt']}"
    for tag in tag_names:
        saved_image.save(Path(opts["storage_img_path"]) / tag / filename)
    gr.Info("Imaginea a fost incarcata cu succes")


def debug_model() -> list:
    if not Identifier.current_model:
        gr.Warning("Selectati un model mai intai")
        return None
    return [weights for weights in Identifier.current_model.values()]


def update_tags() -> gr.CheckboxGroup:
    return gr.CheckboxGroup(choices=get_training_tags())


def add_new_tag(tag_name: str) -> gr.CheckboxGroup:
    create_tag(tag_name)
    return update_tags()


def training_tab():
    with gr.Tab("Etichetare"):
        in_image = gr.ImageEditor(
            type="pil", label="Input", crop_size="1:1", brush=False, eraser=False
        )
        with gr.Group():
            url = gr.Textbox(label="Adresa imagine")
            btn_fetch = gr.Button(value="Descarca")
        with gr.Row():
            with gr.Column():
                with gr.Group():
                    tags = gr.CheckboxGroup(
                        label="Aplica una sau mai multe etichete",
                        choices=get_training_tags(),
                    )
                    gr.Button(value="Reload").click(update_tags, outputs=tags)
                btn_upload = gr.Button(value="Incarca imaginea")
            with gr.Column():
                with gr.Group():
                    new_tag = gr.Textbox(label="Nume eticheta noua")
                    gr.Button(value="Adauga").click(
                        add_new_tag, inputs=[new_tag], outputs=[tags]
                    )
        btn_upload.click(apply_tag, inputs=[in_image, tags])
        btn_fetch.click(fetch_image, inputs=[url], outputs=[in_image])
    with gr.Tab("Antrenare"):
        with gr.Row():
            model_name = gr.Textbox(label="Nume model")
            model_res = gr.Number(
                minimum=32, maximum=256, value=128, label="Rezolutie model"
            )
        btn_train = gr.Button(value="Antreneaza model")
        btn_train.click(Identifier.train, inputs=[model_name, model_res])
    with gr.Tab("Galerie"):
        with gr.Group():
            tags = gr.CheckboxGroup(
                label="Cauta imagini folosind una sau mai multe etichete",
                choices=get_training_tags(),
            )
            gr.Button(value="Reload").click(update_tags, outputs=tags)
        images = gr.Gallery(label="Rezultate")
        tags.input(get_image_paths_for_training_tags, inputs=[tags], outputs=[images])
    with gr.Tab("Debug"):
        gallery_dbg = gr.Gallery()
        btn_dbg = gr.Button(value="Debug")
        btn_dbg.click(debug_model, outputs=[gallery_dbg])
