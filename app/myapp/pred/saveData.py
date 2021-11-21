import pandas
import numpy as np
import os
# taking the list of users and result as input and outputs a cvs file.
# result has the potential user's info and corresponding result
# takes in userID and taskname to create new prediction result file

def saveData(userId='testUser1', predName='testPred', predictList='../../static/dataset/testdatabase.csv', predictResult=np.array([1, 1, 0])):
    df = pandas.read_csv(predictList)
    for i in range(len(df['y'])):
        df.at[i, 'y'] = predictResult[i]
    path = "../../static/results/" + userId
    try:
        os.makedirs(path)
    except FileExistsError:
        # if exists
        pass
    df.to_csv(path + "/" + predName + ".csv")

