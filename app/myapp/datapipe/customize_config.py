import json


# the input should be a dictionary with configurations
def customize_config(customized_configs=''):
    # reads and clear file
    try:
        with open("./config/config.json", "r") as fp:
            configs = json.load(fp)
            for settings in configs:
                configs[settings] = customized_configs[settings]

        with open("./config/config.json", "w+") as fp:
            json.dump(configs, fp)
    except KeyError:
        print('Incorrect configuration data! Please check if the configurations are updated...')


# customize_config({'numFetchRows': 200, 'period': 30})
