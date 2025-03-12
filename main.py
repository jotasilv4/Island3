import json
import warnings

import setproctitle
import os
from fabric import Application
from fabric.utils import get_relative_path
from modules.bar import Bar
from modules.island import Island
from modules.corners import Corners
from config.config import start_config
import config.data as data

fonts_updated_file = f"{data.CACHE_DIR}/fonts_updated"
config_path = os.path.expanduser(f"~/.config/{data.APP_NAME_CAP}/styles/colors.css")

if __name__ == "__main__":
    setproctitle.setproctitle(data.APP_NAME)

    if not os.path.isfile(config_path):
        start_config()

    bar = Bar()
    island = Island()
    bar.island = island
    island.bar = bar
    
    app = Application(f"{data.APP_NAME}", bar, island)

    def set_css():
        app.set_stylesheet_from_file(
            get_relative_path("main.css"),
            exposed_functions={
                "overview_width": lambda: f"min-width: {data.CURRENT_WIDTH * 0.1 * 5 + 92}px;",
                "overview_height": lambda: f"min-height: {data.CURRENT_HEIGHT * 0.1 * 2 + 32 + 56}px;",
            },
        )

    app.set_css = set_css

    app.set_css()
    app.run()
