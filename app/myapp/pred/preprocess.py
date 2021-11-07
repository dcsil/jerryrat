from sklearn import preprocessing

def numeralizeCategory(df):
    lbl = preprocessing.LabelEncoder()
    for i in range(len(df.columns)):
        if df[df.columns[i]].dtype == "object":
            df[df.columns[i]] = lbl.fit_transform(df[df.columns[i]])
    return df
