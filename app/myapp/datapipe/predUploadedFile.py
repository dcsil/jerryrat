from myapp.datapipe.backbone import createBackBone
import os
import pandas
from pathlib import Path


def predictUploadedFile(username, filename):
    backbone = createBackBone(init=True)
    dataset_path = Path(__file__).parent.parent.parent / Path("users/" + username + "/data/" + filename).resolve()

    result_path = Path(__file__).parent.parent.parent / Path("users/" + username + "/result").resolve()
    cleaned_dataset_path = Path(__file__).parent.parent.parent / Path("users/" + username + "/cleaned_data").resolve()

    if not os.path.exists(cleaned_dataset_path):
        os.makedirs(cleaned_dataset_path)
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    cleaned_dataset_path = Path(__file__).parent.parent.parent / Path("users/" + username + "/cleaned_data/" + filename).resolve()
    result_path = Path(__file__).parent.parent.parent / Path("users/" + username + "/result/" + filename).resolve()

    # Start preprocess
    df = pandas.read_csv(dataset_path, index_col=[0])
    df2 = pandas.read_csv(dataset_path)
    personal_info2 = {}
    for i in ["y", "first_name", "last_name", "numbers"]:
        if i != "y":
            personal_info2[i] = df2.pop(i)
        else:
            df2.pop(i)
    for i in ["y", "first_name", "last_name", "numbers"]:
        df.pop(i)
    df.to_csv(cleaned_dataset_path)

    # Start prediction
    result = backbone.predict_database_or_runtime(readOption="local", table_path=cleaned_dataset_path)

    # Generate Result Csv File
    index = []
    for i in range(len(result)):
        index.append(i)
    personal_info2['y'] = result
    # personal_info['index'] = result
    pandas.DataFrame.from_records(personal_info2).to_csv(result_path)


if __name__ == "__main__":
    predictUploadedFile('test1', 'bank-additional-full-with-names-short.csv')
