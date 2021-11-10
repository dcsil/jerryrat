import pyspark
import json
import os

class createBackBone:
    def __init__(self, init=False):
        if init:
            if not os.path.exists("./config"):
                os.makedirs("./config")
            configs = {"numFetchRows": 100, "period": 10, "startdataid": 0}
            with open("./config/config_init.json", "w") as fp:
                json.dump(configs, fp, indent=0)
            with open("./config/config.json", "w") as fp:
                json.dump(configs, fp, indent=0)
        with open("./config/config.json") as fp:
            configs = json.load(fp)
        self.sc = pyspark.SparkContext()
        self.numFetchRows = configs["numFetchRows"]
        self.period = configs["period"]
        self.startdataid = configs["startdataid"]
        #TODO: practice with spark, create a pandas.dataframe from database data periodically (around 10s)

if __name__ == "__main__":
    backbone = createBackBone(init=True)
