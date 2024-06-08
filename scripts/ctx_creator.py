import json
import os
from typing import Dict, Any


def get_config_file_path() -> str:
    scripts_dir = os.getcwd()
    # This is scripts dir. we need config dir, which is near the scripts dir
    config_dir = os.path.join(scripts_dir, os.pardir, "config")

    config_file_name = 'config.json'

    config_path = os.path.join(config_dir, config_file_name)
    return config_path


def get_ctx() -> Dict[str, Any]:
    config_path = get_config_file_path()

    with open(config_path, 'r') as f:
        ctx = json.load(f)

    return ctx
