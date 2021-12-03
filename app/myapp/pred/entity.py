import os
import json

from myapp.pred.customize_config import customize_config
from myapp.pred.load_model import load_model
from myapp.pred.load_config import load_config
from myapp.pred.predict import predict
from myapp.pred.test import test
from myapp.pred.train import train
from pathlib import Path

# interface of the model
class Entity:
    def __init__(self):
        self.model = None
        self.params = None

        # if not os.path.exists("../../../future/checkpoint"):
        #     os.makedirs("../../../future/checkpoint")
        model_path = Path.joinpath(Path(__file__).parent, Path("models/exec/model.json")).resolve()
        config_path = Path.joinpath(Path(__file__).parent, Path("configs/config.json")).resolve()

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

            if not os.path.exists(Path.joinpath(Path(__file__).parent, Path("configs")).resolve()):
                os.makedirs(Path.joinpath(Path(__file__).parent, Path("configs")).resolve())
            with open(Path.joinpath(Path(__file__).parent, Path("configs/config_init.json")).resolve(), 'w') as fp:
                json.dump(self.params, fp, indent=0)
            with open(Path.joinpath(Path(__file__).parent, Path("configs/config.json")), 'w') as fp:
                json.dump(self.params, fp, indent=0)

        if not os.path.exists(Path.joinpath(Path(__file__).parent, Path("models")).resolve()):
            os.makedirs(Path.joinpath(Path(__file__).parent, Path("models")).resolve())
            os.makedirs(Path.joinpath(Path(__file__).parent, Path("models/exec")).resolve())
            os.makedirs(Path.joinpath(Path(__file__).parent, Path("models/schema")).resolve())

        if not self.model:
            self.model = self.train(useDataset=True, model_init=True)

    def train(self, useDataset=False, steps=20, model_init=False, savemodel=True, feedData=None):
        # checkpoint = getCheckpoint()
        model = train(self.model, self.params, useDataset, steps, model_init, savemodel, feedData)
        # setCheckpoint(checkpoint + 1)
        self.model = model

    def customize_config(self, configs={}):
        """
        use this method to customize the model
        """
        customize_config(configs)

    def predict(self, usedataset=False, threshold=0.5, runtimePred=False, feedData=None):
        result = predict(self.model, usedataset, threshold, runtimePred, feedData)
        return result

    def test(self, usedataset=False, threshold=0.5, feedData=None):
        acc = test(self.model, usedataset, threshold, feedData)
        return acc

if __name__ == "__main__":
    entity = Entity()
    entity.train(useDataset=True, model_init=True)
    print(entity.predict(usedataset=True))
    print(entity.test(usedataset=True))
