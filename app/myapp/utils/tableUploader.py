import pandas as pd
from app.myapp.models import Userdata


def tableUploader(filePath):
    class FileNoneError(Exception):
        def __init__(self, file):
            self.file = file

        def __str__(self):
            msg = "The file {} is either not found or does not have a valid extension".format(self.file)
            return msg

    reader = None

    if filePath.endswith(".csv"):
        reader = pd.read_csv(filePath, delimiter=",")
    elif filePath.endswith(".xlsx") or filePath.endswith("xls") or filePath.endswith("xlsx") or \
            filePath.endswith("xlsm") or filePath.endswith("xlsb"):
        reader = pd.read_excel(filePath)
    else:
        raise FileNoneError

    for i, line in enumerate(reader.values.tolist()):
        Userdata.update_or_create(
            age=line[0],
            job=line[1],
            marital=line[2],
            education=line[3],
            default=line[4],
            housing=line[5],
            loan=line[6],
            contact=line[7],
            month=line[8],
            day_of_week=line[9],
            duration=line[10],
            campaign=line[11],
            pdays=line[12],
            previous=line[13],
            poutcome=line[14],
            emp_var_rate=line[15],
            cons_price_idx=line[16],
            cons_conf_idx=line[17],
            euribor3m=line[18],
            nr_employed=line[19],
            y=line[20],
        )
