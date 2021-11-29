from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, desc
from app.myapp.pred.preprocess import numeralizeCategory
import pandas as pd

def readData(user='dv9wgfh46sgcyiil', password='p23it7lf9zqfh3yd', database='syh25csvjgoetrln',
             table="userdata", host='en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', dbtype="mysql",
             connector="mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar",
             driver="com.mysql.cj.jdbc.Driver", port=3306, numRows=5, order='desc', preprocess=True):

    spark = SparkSession.builder.config("spark.jars", connector).getOrCreate()
    sparkdf = spark.read.format("jdbc").option("url", "jdbc:{}://{}:{}/{}".format(dbtype, host, port, database))\
        .option("driver", driver).option("dbtable", table)\
        .option("user", user).option("password", password).load()
    sparkdf = sparkdf.withColumn("index", monotonically_increasing_id())

    if order == 'desc':
        sparkdf = sparkdf.orderBy(desc("index"))

    if numRows != "all" and numRows != -1:
        sparkdf = sparkdf.limit(numRows)

    sparkdf = sparkdf.drop('index')
    df = sparkdf.toPandas()

    df["emp.var.rate"] = pd.to_numeric(df["emp.var.rate"], downcast="float")
    df["cons.price.idx"] = pd.to_numeric(df["cons.price.idx"], downcast="float")
    df["cons.conf.idx"] = pd.to_numeric(df["cons.conf.idx"], downcast="float")
    df["euribor3m"] = pd.to_numeric(df["euribor3m"], downcast="float")
    df["nr.employed"] = pd.to_numeric(df["nr.employed"], downcast="float")

    if preprocess:
        df = numeralizeCategory(df)
    return df

if __name__ == "__main__":
    # Some connection info:

    # database = "jerryratdb"
    # user = "root"
    # password = "zjm19990118"
    # host = "localhost"

    # table = "userdata"
    # connector = "mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar"

    # host = 'en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
    # user = 'dv9wgfh46sgcyiil'
    # password = 'p23it7lf9zqfh3yd'
    # database = 'syh25csvjgoetrln'

    df = readData(user="root", password="zjm19990118", host="localhost", database="jerryratdb", numRows=10, order='desc')
    print(df)
    print(df.dtypes)
