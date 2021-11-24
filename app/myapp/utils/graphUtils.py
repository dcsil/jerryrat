from ..pred.readData import *

ref = {
    'age': 1, 'job': 2, 'marital': 3, 'education': 4, 'default': 5, 'housing': 6, 'loan': 7,
    'month': 9, 'day_of_week': 10, 'campaign': 12, 'pdays': 13, 'previous': 14, 'poutcome': 15
}

def get_graph_data(x, y):
  data = readData()
  x_data = data[x].unique()
  info = {}
  for e in data[y].unique():
    info[e] = [0 for _ in range(len(data[x].unique()))]
  for i, e in enumerate(data[y]):
    key = data[y][i]
    info[key][data[x][i]] += 1
  return x_data, info

def get_metric_idx(metric):
  return ref[metric]
