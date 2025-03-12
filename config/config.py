import os
import json
import shutil
import gi
import config.data as data

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import Image
import toml
from configparser import ConfigParser

CONFIG_DIR = os.path.expanduser(f"~/.config/{data.APP_NAME_CAP}")
WALLPAPERS_DIR_DEFAULT = os.path.expanduser(f"~/.config/{data.APP_NAME_CAP}/assets/wallpapers")

def deep_update(target: dict, update: dict) -> dict:
    """
    Recursively update a nested dictionary with values from another dictionary.
    """
    for key, value in update.items():
        if isinstance(value, dict):
            target[key] = deep_update(target.get(key, {}), value)
        else:
            target[key] = value
    return target

def ensure_matugen_config():
    expected_config = {
        "config": {
            "reload_apps": True,
            "wallpaper": {
                "command": "nitrogen",
                "arguments": ["--restore"],
                "set": True
            }
        },
        "templates": {
            "kyma-shell": {
                "input_path": f"~/.config/{data.APP_NAME_CAP}/config/components/matugen/island-colors.css",
                "output_path": f"~/.config/{data.APP_NAME_CAP}/styles/colors.css",
                "post_hook": (
                    f"fabric-cli exec {data.APP_NAME} 'app.set_css()' &"
                )
            }
        }
    }

    config_path = os.path.expanduser('~/.config/matugen/config.toml')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    existing_config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            existing_config = toml.load(f)

        shutil.copyfile(config_path, config_path + '.bak')

    merged_config = deep_update(existing_config, expected_config)
    with open(config_path, "w") as f:
        toml.dump(merged_config, f)

    current_wall = os.path.expanduser("~/.current.wall")
    if not os.path.exists(current_wall):
        image_path = os.path.expanduser(f"~/.config/{data.APP_NAME_CAP}/assets/wallpapers/example-7.jpg")
        nitro_path = os.path.expanduser("~/.config/nitrogen/bg-saved.cfg")
        
        config = ConfigParser()
        config.read(nitro_path)

        for section in config.sections():
            if "file" not in config[section]:
                config[section]["file"] = image_path
            else:
                config[section]["file"] = image_path

            if "mode" not in config[section]:
                config[section]["mode"] = "0"
            else:
                config[section]["mode"] = "0"
                
        with open(nitro_path, "w") as configfile:
            config.write(configfile)
            
        os.system(f"matugen image {image_path}")

def generate_i3conf() -> str:
    home = os.path.expanduser("~")
    
    i3_config = os.path.expanduser(f"~/.config/{data.APP_NAME_CAP}/config/components/i3/config")
    with open(i3_config, "r") as f:
        config = f.read()

    return config

def start_config():
    ensure_matugen_config()

    i3_config_dir = os.path.expanduser("~/.config/i3/")
    os.makedirs(i3_config_dir, exist_ok=True)

    i3_config_path = os.path.join(i3_config_dir, "config")
    with open(i3_config_path, "w") as f:
        f.write(generate_i3conf())

    os.system("i3-msg reload")

if __name__ == "__main__":
    start_config()