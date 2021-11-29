import json
import os
from readData import readData

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
        self.numFetchRows = configs["numFetchRows"]
        self.period = configs["period"]
        self.startdataid = configs["startdataid"]

    def readData(self, user='dv9wgfh46sgcyiil', password='p23it7lf9zqfh3yd', database='syh25csvjgoetrln',
             table="userdata", host='en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', dbtype="mysql",
             connector="mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar",
             driver="com.mysql.cj.jdbc.Driver", port=3306, order='desc', preprocss=True):
        df = readData(user, password, database, table, host, dbtype, connector, driver, port,
                      self.numFetchRows, order, preprocss)
        return df

    def train_model_with_database(self):
        # TODO: enable training with databse
        pass


if __name__ == "__main__":
    backbone = createBackBone(init=True)
    df = backbone.readData(user="root", password="zjm19990118", host="localhost",
                           database="jerryratdb", preprocss=True)
    print(df)
