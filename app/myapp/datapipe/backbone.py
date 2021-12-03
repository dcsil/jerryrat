import json
import os
from pathlib import Path
import time

from myapp.datapipe.readData import readDataSpark, readDataMySQLConn, readDataLocally
from myapp.pred.entity import Entity

class createBackBone:
    def __init__(self, init=False):
        config_path = Path.joinpath(Path(__file__).parent, Path("config"))
        if init:
            if not os.path.exists(config_path.resolve()):
                os.makedirs(config_path.resolve())
            configs = {"numFetchRows": 100, "period": 1}
            with open((config_path / Path("config_init.json")).resolve(), "w") as fp:
                json.dump(configs, fp, indent=0)
            with open((config_path / Path("config.json")).resolve(), "w") as fp:
                json.dump(configs, fp, indent=0)

        with open((config_path / Path("config.json")).resolve()) as fp:
            configs = json.load(fp)
        self.numFetchRows = configs["numFetchRows"]
        self.period = configs["period"]

    def readData(self, user='dv9wgfh46sgcyiil', password='p23it7lf9zqfh3yd', database='syh25csvjgoetrln',
             table="userdata", host='en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', dbtype="mysql",
             connector="mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar",
             driver="com.mysql.cj.jdbc.Driver", port=3306, order='desc', preprocess=True, readOption="mysql",
                 table_path=None):
        if readOption == "spark":
            df = readDataSpark(user, password, database, table, host, dbtype, connector, driver, port,
                          self.numFetchRows, order, preprocess)
        elif readOption == "mysql":
            df = readDataMySQLConn(host, user, password, database, table, self.numFetchRows, order, preprocess)
        elif readOption == "local":
            df = readDataLocally(table_path)
        return df

    def train_model_database_or_runtime(self, user='dv9wgfh46sgcyiil', password='p23it7lf9zqfh3yd',
                                  database='syh25csvjgoetrln', table="userdata",
                                  host='en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', dbtype="mysql",
                                  connector="mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar",
                                  driver="com.mysql.cj.jdbc.Driver", port=3306, order='desc', preprocess=True,
                                  readOption="mysql", table_path=None, steps=20, savemodel=True):
        # checkpoint = getCheckpoint()
        df = self.readData(user, password, database, table, host, dbtype, connector,
                           driver, port, order, preprocess, readOption, table_path)
        df = df.drop(columns=['dataid'])
        entity = Entity()
        entity.train(steps=steps, savemodel=savemodel, feedData=df, useDataset=False, model_init=False)
        acc = entity.test(usedataset=False, feedData=df)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("accuracy at time {} is {}".format(current_time, acc))


if __name__ == "__main__":
    backbone = createBackBone(init=True)
    df = backbone.readData(user="root", password="zjm19990118", host="localhost",
                           database="jerryratdb", preprocess=True)
    print(df)

    dataset_path = Path(__file__).parent.parent.parent / Path("static/dataset")
    dataset_path = (dataset_path / Path("testdatabase.csv")).resolve()
    df = backbone.readData(readOption="local", table_path=dataset_path)
    print(df)
    print(df.columns)

    backbone.train_model_database_or_runtime(user="root", password="zjm19990118", host="localhost",
                                       database="jerryratdb", savemodel=True)
