import xgboost as xgb


class ModelNotFoundError(Exception):
    def __init__(self, model):
        self.model = model

    def __str__(self):
        msg = "The model {} is not found.".format(self.model)
        return msg


def load_model(model_path="models/model_init.json"):
    model_xgb = xgb.Booster()
    try:
        model_xgb.load_model(model_path)
    except:
        raise ModelNotFoundError(model_path)

    return model_xgb
