import gradio as gr
from .training import training_tab
from .identifier import identifier_tab, model_dropdown
from .options import options_tab

with gr.Blocks(analytics_enabled=False) as app:
    model_dropdown()
    with gr.Tab("Identificator"):
        identifier_tab()
    with gr.Tab("Antrenare identificator"):
        training_tab()
    with gr.Tab("Optiuni"):
        options_tab()
