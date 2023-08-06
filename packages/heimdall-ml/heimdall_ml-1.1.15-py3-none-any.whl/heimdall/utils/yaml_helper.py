import yaml
import os
from typing import Any, Dict, Optional

# the C version is faster, but it doesn't always exist
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


def read_file(*paths):
    contents = ""
    with open(os.path.join(*paths), "r") as fp:
        contents = fp.read()
    return contents


def safe_load(contents) -> Dict[str, Any]:
    return yaml.load(contents, Loader=SafeLoader)


def load_yaml_text(contents) -> Optional[Dict[str, Any]]:
    try:
        return safe_load(contents)
    except (yaml.scanner.ScannerError, yaml.YAMLError) as e:
        raise ValueError(str(e))


def load_yaml_file(path):
    contents = read_file(path)
    return load_yaml_text(contents)
