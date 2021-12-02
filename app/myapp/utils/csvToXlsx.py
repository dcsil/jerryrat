import os
import pandas as pd


def csvToXlsx(csvfile, testMode=False):
    read_file = pd.read_csv(r'{}'.format(csvfile), delimiter=",", encoding='utf-8')
    if not testMode:
        read_file.to_excel(r'{}.xlsx'.format(csvfile[:-4]), index=None, header=True, encoding='utf8')
    else:
        read_file.to_excel(r'{}_test.xlsx'.format(csvfile[:-4]), index=None, header=True, encoding='utf8')


if __name__ == "__main__":
    os.chdir("../../..")
    csvToXlsx("app/static/dataset/testdatabase.csv")
    csvToXlsx("app/static/dataset/testdatabase-with-names.csv")
