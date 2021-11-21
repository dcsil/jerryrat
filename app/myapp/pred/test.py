import numpy as np
import pandas as pd

from myapp.pred.preprocess import numeralizeCategory
import myapp.pred as pred

def test(model, usedataset=False, threshold=0.5):
    result = pred.predict.predict(model, usedataset, threshold)
    acc = 0.0
    if usedataset:  # test on local dataset
        labels = numeralizeCategory(pd.read_csv("../../static/dataset/mvptest/testTarget.csv")).to_numpy()
        acc = np.mean(result == labels)
    else:  # test on data in database
        #TODO: enable tests by database data
        pass
    return acc


if __name__ == "__main__":
    from load_model import load_model
    model = load_model("./models/exec/model_init.json")
    acc = test(model, usedataset=True)
    print(acc)
