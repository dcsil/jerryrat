import json
from pathlib import Path


# the input should be a dictionary with configurations
def customize_config(customized_configs):
    # reads and clear file
    path = (Path(__file__).parent / Path("config/config.json")).resolve()
    print(path)
    try:
        with open(path, "r") as fp:
            configs = json.load(fp)
            for settings in configs:
                if settings in customized_configs:
                    if customized_configs[settings] != "":
                        configs[settings] = customized_configs[settings]
        with open(path, "w+") as fp:
            json.dump(configs, fp)
    except KeyError:
        print('Incorrect configuration data! Please check if the configurations are updated...')
