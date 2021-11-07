import xgboost as xgb
from sklearn.model_selection import train_test_split
import json
import os
import pandas as pd

from load_model import load_model
from load_config import load_config
from preprocess import numeralizeCategory


def train(model_path="./models/exec/model_init.json", config_path="./configs/config_init.json",
          customized_params={}, useDataset=False, steps=20, model_init=False, savemodel=True, checkpoint=0):
    model = None
    params = None
    if not os.path.exists("./checkpoint"):
        os.makedirs("./checkpoint")

    if os.path.exists(model_path):
        model = load_model(model_path)

    if os.path.exists(config_path):
        # TODO: realize param customization page and functionality
        # TODO: use mvpDatabase data
        params = load_config(config_path, customized_params)
    else:
        # default params for init
        params = {
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
        with open('configs/config_init.json', 'w') as fp:
            json.dump(params, fp, indent=0)
    model = train_model(model, params, useDataset, steps)

    # save the init model
    # xgb.save_model: not human readable but loadable for train continuation
    # xgb.dump_model: human readable schema but not loadable for train continuation
    if savemodel:
        if model_init:
            if not os.path.exists("./models"):
                os.makedirs("./models")
                os.makedirs("./models/exec")
                os.makedirs("./models/schema")
            model.save_model("./models/exec/model_init.json")
            model.dump_model("./models/schema/model_init_schema.json")
        else:
            model.save_model("./models/exec/model_{}.json".format(checkpoint))
            model.dump_model("./models/schema/model_{}_schema.json".format(checkpoint))

            # continue training the modek and update by checkpoint + 1
            checkpoint_path = "checkpoint/checkpoint.json"
            with open(checkpoint_path, "w") as fp:
                checkpoint = {"checkpoint": checkpoint}
                json.dump(checkpoint, fp, indent=0)
    return model


def train_model(model, params, useDataset=False, steps=100):
    model = None
    if not useDataset:
        model = train_database(model, params, steps)
    else:
        model = train_locally(model, params, steps)
    return model


def train_locally(model, params, steps):
    # train the init model on local dataset
    # and split into train, test and validation set
    if not os.path.exists("../../static/dataset/mvptest"):
        df1 = pd.read_csv("../../static/dataset/bank-additional.csv")
        df2 = pd.read_csv("../../static/dataset/bank-additional-full.csv")

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

        os.makedirs("../../static/dataset/mvptest")
        otherForDatabaseNoTarget.to_csv("../../static/dataset/mvptest/mvpDatabaseData.csv", index=False)
        otherForDatabaseTarget.to_csv("../../static/dataset/mvptest/mvpDatabaseTarget.csv", index=False)
        trainData.to_csv("../../static/dataset/mvptest/trainData.csv", index=False)
        testData.to_csv("../../static/dataset/mvptest/testData.csv", index=False)
        valData.to_csv("../../static/dataset/mvptest/valData.csv", index=False)
        trainTarget.to_csv("../../static/dataset/mvptest/trainTarget.csv", index=False)
        testTarget.to_csv("../../static/dataset/mvptest/testTarget.csv", index=False)
        valTarget.to_csv("../../static/dataset/mvptest/valTarget.csv", index=False)

        trainData = numeralizeCategory(trainData)
        trainTarget = numeralizeCategory(trainTarget)
        valData = numeralizeCategory(valData)
        valTarget = numeralizeCategory(valTarget)

        D_train = xgb.DMatrix(trainData, label=trainTarget, enable_categorical=True)
        D_val = xgb.DMatrix(valData, label=valTarget, enable_categorical=True)
        model = xgb.train(params, D_train, steps, xgb_model=model, evals=[(D_train, "train"), (D_val, "validation")],
                          early_stopping_rounds=50)
    else:  # data for training, testing and validation have been split
        trainData = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/trainData.csv"))
        trainTarget = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/trainTarget.csv"))
        valData = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/valData.csv"))
        valTarget = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/valTarget.csv"))

        D_train = xgb.DMatrix(trainData, label=trainTarget, enable_categorical=True)
        D_val = xgb.DMatrix(valData, label=valTarget, enable_categorical=True)
        model = xgb.train(params, D_train, steps, xgb_model=model, evals=[(D_train, "train"), (D_val, "validation")],
                          early_stopping_rounds=50)
    return model


def train_database(model, params, steps):
    # TODO: pass train data from the database
    return model


if __name__ == "__main__":
    import shutil

    dirpath = "../../static/dataset/mvptest"
    # test train func when dataset is not initialized
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        train(useDataset=True, model_init=True)
    # test train func when dataset is initialized
    train(useDataset=True, savemodel=True)
