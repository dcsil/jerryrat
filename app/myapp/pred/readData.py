import mysql.connector
import pandas
# import preprocess
# import DB settings
# or not, we can make it remain like it for now, it's enough for an MVP

from sklearn import preprocessing
import numpy as np

def numeralizeCategory(df):
    lbl = preprocessing.LabelEncoder()
    for i in range(len(df.columns)):
        if df[df.columns[i]].dtype == "object":
            df[df.columns[i]] = lbl.fit_transform(df[df.columns[i]])
    return df

def binarizePrediction(prediction, threshold):
    prediction = np.array(prediction)
    prediction[prediction>=threshold] = 1
    prediction[prediction<threshold] = 0
    return prediction

# read from db and return a numeralized data matrix
def readData(host= 'en1ehf30yom7txe7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', user= 'dv9wgfh46sgcyiil', password= 'p23it7lf9zqfh3yd', database= 'syh25csvjgoetrln'):
    mydb = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database
    )
    conn = mydb.cursor()
    conn.execute("SELECT * FROM userdata")
    r = conn.fetchall()
    data = pandas.DataFrame(r)
    # return a numeralized data
    return numeralizeCategory(data)