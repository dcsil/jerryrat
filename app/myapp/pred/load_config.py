import json


class ConfigNotFoundError(Exception):
    def __init__(self, config):
        self.config = config

    def __str__(self):
        msg = "The config {} is not found.".format(self.config)
        return msg


def load_config(config_path="configs/config.json"):
    config = None
    try:
        with open(config_path) as fp:
            config = json.load(fp)
    except FileNotFoundError:
        raise ConfigNotFoundError(config_path)
    except AttributeError:
        raise ConfigNotFoundError(config_path)

    return config
