import gradio as gr
from PIL import Image
from ir import Identifier, Separator
from common.utils import get_model_paths, fetch_image
from common.options import opts
from .parameters import separator_parameters


def model_dropdown() -> gr.Dropdown:
    def update():
        return gr.Dropdown(choices=get_model_paths())

    def load_model(path):
        Identifier.current_model = Identifier.load_from_file(path)
        gr.Info(f"Modelul {str(path)} a fost incarcat")

    drop = gr.Dropdown(interactive=True, label="Model identificator")
    drop.focus(update, outputs=[drop])
    drop.change(load_model, inputs=[drop])
    return drop


def interrogate_model(image: Image) -> dict:
    if not Identifier.current_model:
        gr.Warning("Selectati un model mai intai")
        return None
    results = Identifier.interrogate(
        Identifier.current_model, image, Identifier.Masks.circle
    )
    results = {key: value - min(results.values()) for key, value in results.items()}
    results = {key: value / sum(results.values()) for key, value in results.items()}
    return results


def setup_results():
    components: list = []
    for i in range(10):
        with gr.Group(visible=False) as group:
            components.append(gr.Image(visible=False, width=256))
            components.append(gr.Label(visible=False))
            components.append(group)
    return components


def interrogate(images: list) -> list:
    components: list = []

    if not images:
        gr.Warning("Nu au fost detectate farfurii")
        return setup_results()

    if not Identifier.current_model:
        gr.Info("Selectati un model pentru identificare")

    for i in range(opts["sep_max_plates"]):
        with gr.Group(visible=i < len(images)) as group:
            if i < len(images):
                if images:
                    components.append(
                        gr.Image(visible=i < len(images), value=images[i])
                    )
                else:
                    components.append(gr.Image(visible=False))

                if Identifier.current_model:
                    components.append(
                        gr.Label(
                            visible=i < len(images), value=interrogate_model(images[i])
                        )
                    )
                else:
                    components.append(gr.Label(visible=False))

            else:
                components.append(gr.Image(visible=i < len(images)))
                components.append(gr.Label(visible=i < len(images)))
            components.append(group)
    return components


def interrogate_plate(image: Image) -> list:
    if not image:
        gr.Warning("Introduceti o poza cu o farfurie")
        return setup_results()
    return interrogate([image])


def interrogate_tray(image: Image) -> list:
    if not image:
        gr.Warning("Introduceti o poza cu o tava")
        return setup_results()
    return interrogate(Separator.get_images(image))


def identifier_tab():
    in_image = gr.Image(type="pil", label="Input")
    with gr.Group():
        url = gr.Textbox(label="Adresa imagine")
        btn_fetch = gr.Button(value="Descarca")
    with gr.Accordion("Parametrii separator", open=False):
        separator_parameters()
    with gr.Row():
        btn_iden = gr.Button(value="Identifica farfurie")
        btn_iden_sep = gr.Button(value="Identifica tava")
    with gr.Row():
        results = setup_results()
    btn_iden.click(interrogate_plate, inputs=[in_image], outputs=results)
    btn_iden_sep.click(interrogate_tray, inputs=[in_image], outputs=results)
    btn_fetch.click(fetch_image, [url], in_image)
