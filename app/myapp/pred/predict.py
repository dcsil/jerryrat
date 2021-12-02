import pandas as pd
import xgboost as xgb

from myapp.pred.preprocess import numeralizeCategory, binarizePrediction

def predict(model, usedataset=False, threshold=0.5, runtimePred=False, feedData=None):
    result = None
    if runtimePred:
        #TODO: predict on user's given data
        pass
    else:
        if not usedataset:
            result = predict_database(model, threshold, feedData)
        else:
            result = predict_locally(model, threshold)
    return result

def predict_locally(model, threshold):
    testData = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/testData.csv"))

    D_test = xgb.DMatrix(testData, enable_categorical=True)
    result = model.predict(D_test)
    result = binarizePrediction(result, threshold)

    return result

def predict_database(model, threshold, feedData):
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
