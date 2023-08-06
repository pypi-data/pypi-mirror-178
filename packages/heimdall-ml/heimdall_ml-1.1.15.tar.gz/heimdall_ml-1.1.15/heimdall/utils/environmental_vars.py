import os
import json
from heimdall.utils.errors import DriftAppConfigError


def get_env_string(env_name):
    """
    Loads an string environment variable
    """
    env_str = os.environ.get(env_name)
    if env_str is None:
        raise DriftAppConfigError("Environmental varible " + env_name + " not found")
    return env_str


def get_env_list(env_name):
    """
    Loads an list environment variable
    """
    env_list = json.loads(os.environ.get(env_name))
    if env_list is None:
        raise DriftAppConfigError("Environmental varible " + env_name + " not found")
    return env_list
