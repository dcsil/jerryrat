import pandas as pd
import xgboost as xgb

from load_model import load_model
from preprocess import numeralizeCategory, binarizePrediction

def predict(model_path="./models/exec/model_init.json", usedataset=False, threshold=0.5):
    model = load_model(model_path)
    result = None
    if not usedataset:
        result = predict_database(model, threshold)
    else:
        result = predict_locally(model, threshold)
    return result

def predict_locally(model, threshold):
    testData = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/testData.csv"))
    testTarget = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/testTarget.csv"))

    D_test = xgb.DMatrix(testData, label=testTarget, enable_categorical=True)
    result = model.predict(D_test)
    result = binarizePrediction(result, threshold)

    return result

def predict_database(model, threshold):
    # TODO: connect to data pipeline and feed data from database to model for prediction
    pass


if __name__ == "__main__":
    result = predict(usedataset=True)
    print(result)
