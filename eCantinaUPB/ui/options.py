import gradio as gr
from common.options import save_opts
from common.utils import ensure_dirs
from .parameters import storage_parameters


def save_conf():
    save_opts("options.yml")


def options_tab():
    storage_parameters()
    btn_conf = gr.Button("Salveaza configuratia")
    btn_conf.click(save_conf)
