import names
import random
import csv
import pandas
import numpy as np


def generate_info(length):
    first_names = []
    last_names = []
    numbers = []
    area_codes = [587, 780, 825, 403, 250, 604, 236, 778, 204, 431, 506, 709,
                  867, 782, 902, 867, 249, 343, 416, 519, 647, 905, 365, 548,
                  705, 226, 289, 613, 807, 437, 902, 782, 438, 418, 450, 367,
                  579, 873, 514, 581, 819, 306, 639, 867]
    for i in range(length):
        number = str(random.choice(area_codes))
        number += "-"
        for i in range(7):
            number += str(random.randrange(0, 9))
        first_names.append(names.get_first_name())
        last_names.append(names.get_last_name())
        numbers.append(number)
    return first_names, last_names, numbers


def generate_file(path):
    df = pandas.read_csv(path)
    first_names, last_names, numbers = generate_info(len(df))
    df['first_name'] = first_names
    df['last_name'] = last_names
    df['numbers'] = numbers
    return df


generate_file('../../static/dataset/bank-additional-full.csv').to_csv('../../static/dataset/bank-additional-full-with-names.csv')