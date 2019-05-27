import pickle

def open_pickle(p):
    objs = []
    with open(p, 'rb') as f:
        data = pickle.load(f)
        print(data)

open_pickle('invertedIndex.pickle')
