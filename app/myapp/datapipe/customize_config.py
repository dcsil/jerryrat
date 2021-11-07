import json

def customize_config(customized_configs):
    with open("./config/config.json", "r+") as fp:
        configs = json.load(fp)
        for attr, param in configs:
            configs[attr] = param
        json.dump(configs)
