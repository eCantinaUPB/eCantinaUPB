import gradio as gr
from common.options import opts
from common.utils import ensure_dirs


def parameter(name: str, **config):
    conf: dict = {"value": opts[name], **config}
    component = None

    with gr.Row() as row:
        if type(opts[name]) is int:
            component = gr.Slider(**conf)
        if type(opts[name]) is float:
            component = gr.Slider(**conf)
        if type(opts[name]) is str:
            component = gr.Textbox(**conf)

        if not component:
            raise Exception("Parameter not declared")

        def update_opts(value):
            opts[name] = value
            ensure_dirs()

        if type(component) is gr.Slider:
            component.release(update_opts, inputs=[component])
        if type(component) is gr.Textbox:
            gr.Button(value="Update", scale=0).click(update_opts, inputs=[component])

    return row


def separator_parameters():
    res = parameter(
        "sep_res",
        minimum=64,
        maximum=512,
        step=32,
        label="Rezolutie",
        info="Rezolutia la care separatorul va functiona (afecteaza performanta)",
    )
    alpha = parameter(
        "sep_alpha",
        minimum=0.0,
        maximum=3.0,
        step=0.05,
        label="Alpha",
        info="Control contrast",
    )
    beta = parameter(
        "sep_beta",
        minimum=0.0,
        maximum=3.0,
        step=0.05,
        label="Beta",
        info="Control luminozitate",
    )
    gauss_ker_size = parameter(
        "sep_gauss_ker_size",
        minimum=1,
        maximum=25,
        step=2,
        label="Dimensiune blur gaussian",
        info="Dimensiunea nucleului folosit pentru blur gaussian",
    )
    gauss_sigma = parameter(
        "sep_gauss_sigma",
        minimum=1,
        maximum=100,
        step=1,
        label="Sigma Gauss",
        info="Deviatia pentru filtrul gaussian",
    )
    canny_max = parameter(
        "sep_canny_max",
        minimum=1,
        maximum=200,
        step=1,
        label="Maxim Canny",
        info="Pragul superior pentru detectarea marginilor cu Canny",
    )
    hough_mindist = parameter(
        "sep_hough_mindist",
        minimum=0,
        maximum=opts["sep_res"] / 2,
        step=1,
        label="Distanta minima Hough",
        info="Distanta minima dintre cercuri",
    )
    hough_minr = parameter(
        "sep_hough_minr",
        minimum=0,
        maximum=opts["sep_res"] / 2,
        step=1,
        label="Raza minima Hough",
        info="Raza minima a cercurilor detectate",
    )
    hough_maxr = parameter(
        "sep_hough_maxr",
        minimum=0,
        maximum=opts["sep_res"] / 2,
        step=1,
        label="Raza maxima Hough",
        info="Raza maxima a cercurilor detectate",
    )
    hough_cen = parameter(
        "sep_hough_cen",
        minimum=1,
        maximum=300,
        step=1,
        label="Prag voturi Hough",
        info="Pragul superior al numarului de voturi necesare pentru a considera un cerc",
    )


def storage_parameters():
    sep_max_plates = parameter(
        "sep_max_plates",
        minimum=1,
        maximum=16,
        step=1,
        label="Numar maxim farfurii",
        info="Numarul maxim de farfurii ce vor fi afisate",
    )
    storage_img_path = parameter(
        "storage_img_path",
        label="Directoriu imagini antrenament",
        info="Directoriul in care vor fi salvate imaginile pentru antrenament",
    )
    storage_img_res = parameter(
        "storage_img_res",
        minimum=32,
        maximum=1024,
        step=32,
        label="Rezolutie imagini antrenament",
        info="Rezolutia imaginilor pentru antrenament",
    )
    storage_img_fmt = parameter(
        "storage_img_fmt",
        label="Format imagini",
        info="Formatul in care vor fi salvate imaginile (png/jpg/webp)",
    )
    storage_model_path = parameter(
        "storage_model_path",
        label="Directoriu modele",
        info="Directoriul in care vor fi salvate modelele pentru identificator",
    )
