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

def dropUserContactInfo(df):
    if 'first_name' in df.columns:
        df = df.drop(columns=['first_name'])
    if 'last_name' in df.columns:
        df = df.drop(columns=['last_name'])
    if 'numbers' in df.columns:
        df = df.drop(columns=['numbers'])
    return df
