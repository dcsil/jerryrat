import json
import os
from pathlib import Path
import time

from myapp.datapipe.readData import readDataSpark, readDataMySQLConn, readDataFromRuntimeUpload
from myapp.pred.entity import Entity

class createBackBone:
    def __init__(self, init=False, user='dv9wgfh46sgcyiil', password='p23it7lf9zqfh3yd', database='syh25csvjgoetrln',
             table="userdata", host='en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', dbtype="mysql",
             connector="myapp/datapipe/mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar",
             driver="com.mysql.cj.jdbc.Driver", port=3306):
        config_path = Path.joinpath(Path(__file__).parent, Path("config"))
        if init:
            if not os.path.exists(config_path.resolve()):
                os.makedirs(config_path.resolve())
            configs = {"numFetchRows": 100, "period": 1}
            with open((config_path / Path("config_init.json")).resolve(), "w") as fp1:
                json.dump(configs, fp1, indent=0)
            with open((config_path / Path("config.json")).resolve(), "w") as fp2:
                json.dump(configs, fp2, indent=0)

        with open((config_path / Path("config.json")).resolve()) as fp:
            configs = json.load(fp)
        self.numFetchRows = configs["numFetchRows"]
        self.period = configs["period"]
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.host = host
        self.dbtype = dbtype
        self.connector = connector
        self.driver = driver
        self.port = port

    def readData(self, order='desc', preprocess=True, readOption="mysql", table_path=None):
        if readOption == "spark":
            df = readDataSpark(self.user, self.password, self.database, self.table, self.host, self.dbtype,
                               self.connector, self.driver, self.port, self.numFetchRows, order, preprocess)
        elif readOption == "mysql":
            df = readDataMySQLConn(self.host, self.user, self.password, self.database, self.table,
                                   self.numFetchRows, order, preprocess)
        elif readOption == "local":
            df = readDataFromRuntimeUpload(table_path, preprocess)
        return df

    # database: read data from database
    # runtime: read data given by customer
    def train_model_database_or_runtime(self, order='desc', preprocess=True, readOption="mysql", table_path=None,
                                        steps=20, savemodel=True):
        # checkpoint = getCheckpoint()
        df = self.readData(order, preprocess, readOption, table_path)
        if 'dataid' in df.columns:
            df = df.drop(columns=['dataid'])
        entity = Entity()
        entity.train(steps=steps, savemodel=savemodel, feedData=df, usedataset=False, model_init=False)
        acc = entity.test(usedataset=False, feedData=df)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("accuracy at time {} is {}".format(current_time, acc))

    # database: read data from database
    # runtime: read data given by customer
    def predict_database_or_runtime(self, order='desc', preprocess=True, readOption="mysql", table_path=None,
                                    threshold=0.5):
        # checkpoint = getCheckpoint()
        df = self.readData(order, preprocess, readOption, table_path)
        if 'dataid' in df.columns:
            df = df.drop(columns=['dataid'])
        entity = Entity()
        result = entity.predict(usedataset=False, threshold=threshold, feedData=df)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("make prediction on {}".format(current_time))
        return result

    # database: read data from database
    # runtime: read data given by customer
    # runtime parameter: if make test by data from customer or database,
    # if not, make test by local dataset
    def test_database_or_runtime(self, order='desc', preprocess=True,
                                  readOption="mysql", table_path=None, threshold=0.5, runtime=True):
        # checkpoint = getCheckpoint()
        df = self.readData(order, preprocess, readOption, table_path)
        if 'dataid' in df.columns:
            df = df.drop(columns=['dataid'])
        entity = Entity()
        acc = entity.test(usedataset=False, threshold=threshold, runTimeTest=runtime, feedData=df)

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("accuracy at time {} is {}".format(current_time, acc))
        return acc


if __name__ == "__main__":
    backbone = createBackBone(init=True)
    '''
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
    '''

    dataset_path = Path(__file__).parent.parent.parent / Path("static/dataset")
    dataset_path = (dataset_path / Path("testdatabase.csv")).resolve()
    result = backbone.predict_database_or_runtime(readOption="local", table_path=dataset_path)
    print(result)

    '''
    result = backbone.test_database_or_runtime(user="root", password="zjm19990118", host="localhost",
                           database="jerryratdb", preprocess=True, runtime=True)
    print(result)
    '''
    # df = backbone.readData(user="root", password="zjm19990118", host="localhost",
    #                        database="jerryratdb", preprocess=True, readOption='spark')
    # print(df)
