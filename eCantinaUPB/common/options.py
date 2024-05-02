from pathlib import Path
import logging
import yaml

version: str = "0.8b"

default_opts: dict = {
    "sep_res": 256,
    "sep_alpha": 1.3,
    "sep_beta": 1.0,
    "sep_gauss_ker_size": 3,
    "sep_gauss_sigma": 5,
    "sep_canny_max": 20,
    "sep_hough_mindist": 70,
    "sep_hough_minr": 10,
    "sep_hough_maxr": 128,
    "sep_hough_cen": 50,
    "sep_max_plates": 16,
    "storage_img_path": str(Path("data/img")),
    "storage_img_res": 512,
    "storage_img_fmt": "png",
    "storage_model_path": str(Path("data/models")),
    "log_level": 20,
}

opts = default_opts.copy()


def load_opts(path: Path):
    global opts
    try:
        with open(path, "r") as file:
            loaded_opts = yaml.safe_load(file) or {}
            opts = {**loaded_opts, **default_opts}
    except FileNotFoundError:
        opts = default_opts.copy()
        save_opts(path)

    logging.basicConfig(level=opts["log_level"])
    logging.info(f"Starting eCantinaUPB v{version}")


def save_opts(path: Path):
    with open(path, "w") as file:
        yaml.dump(opts, file)
