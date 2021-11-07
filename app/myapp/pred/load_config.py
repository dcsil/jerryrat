import json


def load_config(config_path="configs/config_init.json", customized_params={}):
    class ConfigNotFoundError(Exception):
        def __init__(self, config):
            self.config = config

        def __str__(self):
            msg = "The config {} is not found.".format(self.config)
            return msg

    config = None
    try:
        with open(config_path) as fp:
            config = json.load(fp)
        for attr, param in customized_params.items():
            config[attr] = param
    except FileNotFoundError:
        raise ConfigNotFoundError(config_path)
    except AttributeError:
        raise ConfigNotFoundError(config_path)

    return config
