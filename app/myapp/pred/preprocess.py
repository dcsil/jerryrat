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
