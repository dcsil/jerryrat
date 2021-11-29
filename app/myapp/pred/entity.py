import os
import json

from checkpoint import getCheckpoint
from customize_config import customize_config
from load_model import load_model
from load_config import load_config
from predict import predict
from test import test
from train import train

# interface of the model
class Entity:
    def __init__(self, model_path="./models/exec/model_init.json", config_path="./configs/config_init.json"):
        self.model = None
        self.params = None

        if not os.path.exists("./checkpoint"):
            os.makedirs("./checkpoint")

        if os.path.exists(model_path):
            self.model = load_model(model_path)

        if os.path.exists(config_path):
            self.params = load_config(config_path)
        else:
            # default params for init
            self.params = {
                "eta": 0.3,  # learning_rate
                "gamma": 0,  # min_split_loss
                "objective": 'binary:logistic',  # loss function
                "max_depth": 6,
                "nthread": 4,
                "eval_metric": 'auc',
                "lambda": 1,  # L2 regularization
            }

            if not os.path.exists('./configs'):
                os.makedirs('./configs')
            with open('./configs/config_init.json', 'w') as fp:
                json.dump(self.params, fp, indent=0)
            with open('./configs/config.json', 'w') as fp:
                json.dump(self.params, fp, indent=0)

        if not os.path.exists("./models"):
            os.makedirs("./models")
            os.makedirs("./models/exec")
            os.makedirs("./models/schema")

        checkpoint_path = "checkpoint/checkpoint.json"
        if not os.path.exists("checkpoint/checkpoint.json"):
            with open(checkpoint_path, "w") as fp:
                checkpoint = {"checkpoint": 0}
                json.dump(checkpoint, fp, indent=0)

        if not self.model:
            self.model = self.train(useDataset=True, model_init=True)

    def train(self, useDataset=False, steps=20, model_init=False, savemodel=True):
        checkpoint = getCheckpoint()
        model = train(self.model, self.params, useDataset, steps, model_init, savemodel, checkpoint)
        self.model = model

    def customize_config(self, configs={}):
        """
        use this method to customize the model
        """
        customize_config(configs)

    def predict(self, usedataset=False, threshold=0.5):
        result = predict(self.model, usedataset, threshold)
        return result

    def test(self, usedataset=False, threshold=0.5):
        acc = test(self.model, usedataset, threshold)
        return acc

if __name__ == "__main__":
    entity = Entity()
    entity.train(useDataset=True, model_init=True)
    print(entity.predict(usedataset=True))
    print(entity.test(usedataset=True))
