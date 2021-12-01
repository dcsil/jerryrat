import mysql.connector
from myapp.datapipe.readData import readDataSpark
import pandas
# import preprocess
# import DB settings
# or not, we can make it remain like it for now, it's enough for an MVP

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
    # return numeralizeCategory(data)
    return data
