import numpy as np
import pandas as pd
from pathlib import Path

from myapp.pred.preprocess import numeralizeCategory
from myapp.pred.predict import predict

def test(model, usedataset=False, threshold=0.5, runTimeTest=False, feedData=None):
    result = predict(model, usedataset, threshold, feedData)
    labels = None
    acc = 0.0
    # NOTE: this part is only used for test purpose by reading the local data
    # and will not be used in runtime
    if not runTimeTest:
        testset_path = Path("static/dataset/mvptest/testTarget.csv")
        labels = numeralizeCategory(pd.read_csv(Path.joinpath(Path(__file__).parent.parent.parent,
                                                              testset_path).resolve())).to_numpy()
    else:
        assert (not (feedData is None))
        assert ('y' in feedData.columns)
        labels = numeralizeCategory(feedData['y'].to_frame()).to_numpy()
    acc = np.mean(result == labels)
    return acc


if __name__ == "__main__":
    from load_model import load_model
    model = load_model("./models/exec/model_init.json")
    acc = test(model, usedataset=True)
    print(acc)
