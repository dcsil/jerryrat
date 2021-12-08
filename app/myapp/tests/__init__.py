from django.contrib.auth import get_user_model
import pandas
import os

# create temporary account if not exist
try:
    User = get_user_model()
    user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
except Exception as e:
    pass

dic = {'age': [56],
       'job': ['services'],
       'marital': ['married'],
       'education': ['basic.4y'],
       'default': ['no'],
       'housing': ['no'],
       'loan': ['no'],
       'contact': ['telephone'],
       'month': ['may'],
       'day_of_week': ['mon'],
       'duration': [61],
       'campaign': [1],
       'pdays': [999],
       'previous': [0],
       'poutcome': ['nonexistent'],
       'emp.var.rate': [1.1],
       'cons.price.idx': [93.994],
       'cons.conf.idx': [-36.4],
       'euribor3m': [4.857],
       'nr.employed': [5191],
       'y': ['no'],
       'first_name': ['Pony'],
       'last_name': ['Ma'],
       'numbers': ['416-0246436']
       }

# create test data if not exist
if os.path.exists("./users/temporary/data/test-campaign1.csv"):
    pass
else:
    print("==================Creating test File==================")
    pandas.DataFrame.from_dict(dic).to_csv("./users/temporary/data/test-campaign1.csv", index=False)
