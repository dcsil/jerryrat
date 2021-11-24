from ..pred.readData import *

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