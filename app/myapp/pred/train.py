import xgboost as xgb
from sklearn.model_selection import train_test_split
# import json
import os
import pandas as pd
from pathlib import Path
import time

from myapp.pred.load_model import load_model
from myapp.pred.preprocess import numeralizeCategory


def train(model=None, params=None, useDataset=False, steps=20, model_init=False, savemodel=True, feedData=None):

    model = train_model(model, params, useDataset, steps, feedData)

    # save the init model
    # xgb.save_model: not human readable but loadable for train continuation
    # xgb.dump_model: human readable schema but not loadable for train continuation
    if savemodel:
        if model_init:

            model.save_model(Path.joinpath(Path(__file__).parent, Path("models/exec/model_init.json")).resolve())
            model.dump_model(Path.joinpath(Path(__file__).parent,
                                           Path("models/schema/model_init_schema.json.json")).resolve())
        else:
            model.save_model(Path.joinpath(Path(__file__).parent, Path("models/exec/model.json")).resolve())
            model.dump_model(Path.joinpath(Path(__file__).parent,
                                           Path("models/schema/model_schema.json.json")).resolve())

            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)

            # continue training the model and update by checkpoint + 1
            # checkpoint_path = "../../../future/checkpoint/checkpoint.json"
            # if not os.path.exists(checkpoint_path):
            #     with open(checkpoint_path, "w") as fp:
            #         checkpoint = {"checkpoint": checkpoint}
            #         json.dump(checkpoint, fp, indent=0)
        print("model saved at time {}".format(current_time))
    return model


def train_model(model=None, params=None, useDataset=False, steps=100, feedData=None):
    if not useDataset:
        assert not (feedData is None)
        model = train_database_or_runtime(model, params, steps, feedData)
    else:
        model = train_locally(model, params, steps)
    return model

# NOTE: this function is only for initializing the model
# and will not be used in runtime
def train_locally(model, params, steps):
    # train the init model on local dataset
    # and split into train, test and validation set
    dataset_path = Path(__file__).parent.parent.parent / Path("static/dataset")

    if not os.path.exists((dataset_path / Path("mvptest")).resolve()):
        df1 = pd.read_csv((dataset_path / Path("bank-additional.csv")).resolve())
        df2 = pd.read_csv((dataset_path / Path("bank-additional-full.csv")).resolve())

        df_all = pd.concat([df1, df2])
        trainValTest = df_all.iloc[0:25000]
        otherForDatabase = df_all.iloc[25000:]

        # split target and other data
        trainValTestTarget = trainValTest["y"]
        otherForDatabaseTarget = otherForDatabase["y"]
        trainValTestNoTarget = trainValTest.drop(columns=["y"])
        otherForDatabaseNoTarget = trainValTest.drop(columns=["y"])

        # train test validation split
        trainData, testData, trainTarget, testTarget = train_test_split(trainValTestNoTarget, trainValTestTarget,
                                                                        train_size=0.7, shuffle=False)
        testData, valData, testTarget, valTarget = train_test_split(testData, testTarget, test_size=1 / 3,
                                                                    shuffle=True, random_state=101)
        trainTarget = trainTarget.to_frame()
        testTarget = testTarget.to_frame()
        valTarget = valTarget.to_frame()

        os.makedirs((dataset_path / Path("mvptest")).resolve())
        otherForDatabaseNoTarget.to_csv((dataset_path / Path("mvptest/mvpDatabaseData.csv")).resolve(), index=False)
        otherForDatabaseTarget.to_csv((dataset_path / Path("mvptest/mvpDatabaseTarget.csv")).resolve(),
                                      index=False)
        trainData.to_csv((dataset_path / Path("mvptest/trainData.csv")).resolve(), index=False)
        testData.to_csv((dataset_path / Path("mvptest/testData.csv")).resolve(), index=False)
        valData.to_csv((dataset_path / Path("mvptest/valData.csv")).resolve(), index=False)
        trainTarget.to_csv((dataset_path / Path("mvptest/trainTarget.csv")).resolve(), index=False)
        testTarget.to_csv((dataset_path / Path("mvptest/testTarget.csv")).resolve(), index=False)
        valTarget.to_csv((dataset_path / Path("mvptest/valTarget.csv")).resolve(), index=False)

        trainData = numeralizeCategory(trainData)
        trainTarget = numeralizeCategory(trainTarget)
        valData = numeralizeCategory(valData)
        valTarget = numeralizeCategory(valTarget)

        D_train = xgb.DMatrix(trainData, label=trainTarget, enable_categorical=True)
        D_val = xgb.DMatrix(valData, label=valTarget, enable_categorical=True)
        model = xgb.train(params, D_train, steps, xgb_model=model, evals=[(D_train, "train"), (D_val, "validation")],
                          early_stopping_rounds=50)
    else:  # data for training, testing and validation have been split
        trainData = numeralizeCategory(pd.read_csv((dataset_path / Path("mvptest/trainData.csv")).resolve()))
        trainTarget = numeralizeCategory(pd.read_csv((dataset_path / Path("mvptest/trainTarget.csv")).resolve()))
        valData = numeralizeCategory(pd.read_csv((dataset_path / Path("mvptest/valData.csv")).resolve()))
        valTarget = numeralizeCategory(pd.read_csv((dataset_path / Path("mvptest/valTarget.csv")).resolve()))

        D_train = xgb.DMatrix(trainData, label=trainTarget, enable_categorical=True)
        D_val = xgb.DMatrix(valData, label=valTarget, enable_categorical=True)
        model = xgb.train(params, D_train, steps, xgb_model=model, evals=[(D_train, "train"), (D_val, "validation")],
                          early_stopping_rounds=50)
    return model


def train_database_or_runtime(model, params, steps, feedData):
    dataset_path = Path(__file__).parent.parent.parent / Path("static/dataset")
    valData = numeralizeCategory(pd.read_csv((dataset_path / Path("mvptest/valData.csv")).resolve()))
    valTarget = numeralizeCategory(pd.read_csv((dataset_path / Path("mvptest/valTarget.csv")).resolve()))

    D_train = xgb.DMatrix(feedData.drop(columns=['y']), label=feedData["y"].to_frame(), enable_categorical=True)
    D_val = xgb.DMatrix(valData, label=valTarget, enable_categorical=True)
    model = xgb.train(params, D_train, steps, xgb_model=model, evals=[(D_train, "train"), (D_val, "validation")],
                      early_stopping_rounds=50)
    return model


if __name__ == "__main__":
    import shutil

    dirpath = (Path(__file__).parent.parent.parent / Path("static/dataset/mvptest")).resolve()
    params = {
        "eta": 0.3,  # learning_rate
        "gamma": 0,  # min_split_loss
        "objective": 'binary:logistic',  # loss function
        "max_depth": 6,
        "nthread": 4,
        "eval_metric": 'auc',
        "lambda": 1,  # L2 regularization
    }
    # test train func when dataset is not initialized
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        train(params=params, useDataset=True, model_init=True)
    # test train func when dataset is initialized
    model = load_model((Path(__file__).parent / Path("models/exec/model_init.json")).resolve())
    train(params=params, model=model, useDataset=True)
