import mysql.connector
import pandas
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

ref = {
    'age': 1, 'job': 2, 'marital': 3, 'education': 4, 'default': 5, 'housing': 6, 'loan': 7,
    'month': 9, 'day_of_week': 10, 'campaign': 12, 'pdays': 13, 'previous': 14, 'poutcome': 15
}

def get_graph_data(x, y):
  data = readData()
  x_data = data[x].unique()
  info = {}
  for e in data[y].unique():
    info[e] = [0 for _ in range(len(data[x].unique()))]
  for i, e in enumerate(data[y]):
    key = data[y][i]
    x_val = data[x][i]
    x_idx = np.where(x_data == x_val)[0][0]
    info[key][x_idx] += 1
  return x_data, info

def get_metric_idx(metric):
  return ref[metric]


if __name__ == "__main__":
    df = readData(user="root", password="zjm19990118", host="localhost", database="jerryratdb")
    print(df.dtypes)
