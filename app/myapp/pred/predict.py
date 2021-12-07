import pandas as pd
import xgboost as xgb
from pathlib import Path

from myapp.pred.preprocess import numeralizeCategory, binarizePrediction

def predict(model, usedataset=False, threshold=0.5, feedData=None):
    result = None
    if not usedataset:
        result = predict_database_or_runtime(model, threshold, feedData)
    else:
        result = predict_locally(model, threshold)
    return result


# NOTE: this function is only used for test purpose by reading the local data
# and will not be used in runtime
def predict_locally(model, threshold):
    dataset_path = Path(__file__).parent.parent.parent / Path("static/dataset")
    testData = numeralizeCategory(pd.read_csv((dataset_path / Path("mvptest/testData.csv")).resolve()))

    D_test = xgb.DMatrix(testData, enable_categorical=True)
    result = model.predict(D_test)
    result = binarizePrediction(result, threshold)

    return result

def predict_database_or_runtime(model, threshold, feedData):
    assert (not (feedData is None))

    if 'y' in feedData.columns:
        D_pred = xgb.DMatrix(feedData.drop(columns=["y"]), enable_categorical=True)
    else:
        D_pred = xgb.DMatrix(feedData, enable_categorical=True)
    result = model.predict(D_pred)
    result = binarizePrediction(result, threshold)
    return result


if __name__ == "__main__":
    from load_model import load_model
    model = load_model("./models/exec/model_init.json")
    result = predict(model, usedataset=True)
    print(result)
