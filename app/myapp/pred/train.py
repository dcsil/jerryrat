import xgboost as xgb
from sklearn.model_selection import train_test_split
import json

from load_model import load_model

def train(model_path="models/model_init.json", config_path="configs/config_init.json"):
    model = load_model(model_path)

if __name__ == "__main__":
    pass