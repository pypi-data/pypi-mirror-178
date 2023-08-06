import json
import pathlib
import typing as t

import mantik.unicore.exceptions as exceptions
import yaml

_ALLOWED_FILE_EXTENSIONS = {"json": [".json"], "yaml": [".yml", ".yaml"]}


def read_config(path: pathlib.Path) -> t.Dict:
    if path.suffix in _ALLOWED_FILE_EXTENSIONS["json"]:
        return _read_json_config(path)
    elif path.suffix in _ALLOWED_FILE_EXTENSIONS["yaml"]:
        return _read_yaml_config(path)
    raise exceptions.UnsupportedFileTypeException(
        f"Unsupported file type for config {path.suffix}"
    )


def _read_yaml_config(backend_config_path: pathlib.Path) -> t.Dict:
    with open(backend_config_path, "r") as f:
        return yaml.safe_load(f)


def _read_json_config(backend_config_path: pathlib.Path) -> t.Dict:
    with open(backend_config_path, "r") as f:
        return json.load(f)
