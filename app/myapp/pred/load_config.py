import json

def load_config(config_path="configs/config_init.json"):
    class ConfigNotFoundError(Exception):
        def __init__(self, config):
            self.config = config

        def __str__(self):
            msg = "The config {} is not found.".format(self.config)
            return msg

    config = None
    try:
        json.load(config_path)
    except:
        raise ConfigNotFoundError(config_path)

    return config