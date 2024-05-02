from ui import app
from common.options import load_opts
from common.utils import ensure_dirs

if __name__ == "__main__":
    load_opts("options.yml")
    ensure_dirs()
    app.launch()
