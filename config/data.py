import os
import json
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, GLib  # noqa: E402
from fabric.utils.helpers import get_relative_path  # noqa: E402


gi.require_version("Gtk", "3.0")

APP_NAME = "island3"
APP_NAME_CAP = "Island3"

CACHE_DIR = str(GLib.get_user_cache_dir()) + f"/{APP_NAME}"

USERNAME = os.getlogin()
HOSTNAME = os.uname().nodename
HOME_DIR = os.path.expanduser("~")

screen = Gdk.Screen.get_default()
CURRENT_WIDTH = screen.get_width()
CURRENT_HEIGHT = screen.get_height()

default_wallpapers_dir = get_relative_path("../assets/wallpapers")
CONFIG_FILE = os.path.expanduser(f"~/.config/{APP_NAME_CAP}/styles/colors.css")

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    WALLPAPERS_DIR = config.get("wallpapers_dir", default_wallpapers_dir)
else:
    WALLPAPERS_DIR = default_wallpapers_dir