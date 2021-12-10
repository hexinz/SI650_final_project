from pyserini.index import IndexReader
from tqdm import tqdm, trange
import sys
import numpy as np
import pandas as pd
from collections import Counter
import pickle
from pyserini.index import IndexReader
import json

index_reader = IndexReader('./transcripts/indexes')
idx = range(54936)


class Ranker(object):
    '''
    The base class for ranking functions. Specific ranking functions should
    extend the score() function, which returns the relevance of a particular
    document for a given query.
    '''

    def __init__(self, index_reader, tf, N, df, dl, avg_dl):
        self.index_reader = index_reader
        self.tf = tf
        self.N = N
        self.df = df
        self.dl = dl
        self.avg_dl = avg_dl

    def score(self, query, doc_id, k1=1.5, b=0.5, k3=1.2):
        rank_score = 0
        return rank_score

class BM25Ranker(Ranker):

    def __init__(self, index_reader, tf, N, df, dl, avg_dl):
        super().__init__(index_reader, tf, N, df, dl, avg_dl)
        # NOTE: the reader is stored as a field of the subclass and you can
        # compute and cache any intermediate data in the constructor to save for
        # later (HINT: Which values in the ranking are constant across queries
        # and documents?)

    def score(self, query, doc_id, k1=1.5, b=0.5, k3=1.2):
        rank_score = 0
        # get query term frequency
        qtf = Counter(query)
        for word in query:
            if self.tf[doc_id].get(word):
                rank_score += np.log((self.N - self.df.get(word, 0) + 0.5) / (self.df.get(word, 0) + 0.5)) * (k1 + 1) * self.tf[doc_id][word] / \
                              (k1 * (1 - b + b * self.dl[doc_id] / self.avg_dl) + self.tf[doc_id][word]) * (k3 + 1) * qtf[word] / \
                              (k3 + qtf[word])

        #     print(i,rank_score)
        return rank_score

class Retrival_Interface():
    def __init__(self, retrieve_num):
        self.retrieve_num = retrieve_num

    def Retrival(self, query):
        with open('file.pickle', 'rb') as file:
            # Create file.pickle in advance in jupyter notebook
            # with open('file.pickle', 'wb') as file:
            #     # A new file will be created
            #     pickle.dump(tf, file)
            #     pickle.dump(N, file)
            #     pickle.dump(df, file)
            #     pickle.dump(dl, file)
            #     pickle.dump(avg_dl, file)
            # Call load method to deserialze
            tf = pickle.load(file)
            N = pickle.load(file)
            df = pickle.load(file)
            dl = pickle.load(file)
            avg_dl = pickle.load(file)

        ranker = BM25Ranker(index_reader, tf, N, df, dl, avg_dl)
        # DocumentId = []
        # Score = []
        # Raw = []
        result = []
        analyzed_query = index_reader.analyze(query)
        rel_score = []
        for docid in idx:
            rel_score.append(ranker.score(analyzed_query, docid))
        relevant = np.argsort(rel_score)[::-1][:self.retrieve_num]
        # DocumentId += [idx[r] for r in relevant]
        # Score += [rel_score[r] for r in relevant]
        # Raw += [json.loads(index_reader.doc(str(idx[r])).raw())['contents'] for r in relevant]
        # result = dict({'DocumentId': DocumentId, 'Score': Score, 'Raw': Raw})
        for r in relevant:
            result.append([idx[r], rel_score[r], json.loads(json.loads(index_reader.doc(str(idx[r])).raw())['contents'])['line']])
        return result

test = Retrival_Interface(10)
result = test.Retrival('Sheldon idiot')
print(result)