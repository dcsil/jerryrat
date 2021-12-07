import json


# the input should be a dictionary with configurations
def customize_config(customized_configs, user):
    # reads and clear file
    path = './users/' + user + '/config/config.json'
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


def customize_config(customized_configs):
    # reads and clear file
    path1 = './myapp/datapipe/config/config.json'
    path2 = './myapp/pred/configs/config.json'
    try:
        for path in [path1, path2]:
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

