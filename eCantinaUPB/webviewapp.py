import threading
from ui import app
import webview
from common.options import load_opts
from common.utils import ensure_dirs


def start_gradio():
    app.launch()


if __name__ == "__main__":
    load_opts("options.yml")
    ensure_dirs()
    gradio_thread = threading.Thread(target=start_gradio)
    gradio_thread.daemon = True
    gradio_thread.start()
    webview.create_window("eCantinaUPB", "http://127.0.0.1:7860")
    webview.start()
