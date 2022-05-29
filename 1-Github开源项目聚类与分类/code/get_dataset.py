import numpy as np
import pandas as pd
from read_data import read_data

class Dataset:
    def __init__(self, vec, data):
        self.vec = vec
        self.data = data
    def __getitem__(self, index):
        return (self.vec[index], self.data[index])

def get_dataset(penalty_func = None):
    print('Now loading text data...')
    repo_name, repo_data = read_data()
    
    print('Now loading contribute vector data, this may take minutes.')
    action = pd.read_csv('./data_csv/Action.csv')
    vec = []
    num_classes = len(action['modularity_class'].unique())
    for repo_id in repo_name:
        vec_item = np.zeros((num_classes,))
        series = action.loc[action['repo_id'] == repo_id]
        group = series.groupby('modularity_class')
        idx = np.array(list(group.indices.keys())).astype('int')
        # print(np.array(list(group.indices.keys())).astype('int'))
        if penalty_func != None:
            vec_item[idx] = penalty_func(np.array(group.sum()['score']))
        else:
            vec_item[idx] = np.sqrt(np.array(group.sum()['score']))
        # print(vec_item[vec_item > 0])
        vec.append(vec_item)

    vec = np.array(vec)
    print('Text data\'s length: ', len(repo_data))
    print('Vector\'s shape: ', vec.shape)
    
    return Dataset(vec, repo_data), repo_name