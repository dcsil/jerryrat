import xgboost as xgb
from sklearn.model_selection import train_test_split
import json
import os

from load_model import load_model
from load_config import load_config

def train(model_path="models/model_init.json", config_path="configs/config_init.json"):
    model = None
    params = None
    if os.path.exists(model_path):
        model = load_model(model_path)
    if os.path.exists:
        params = load_config(config_path)
    else:
        params = {

        }


if __name__ == "__main__":
    pass