import pandas as pd
import csv
from requests import get
import json
from datetime import datetime, timedelta, date
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
from scipy.stats import pearsonr

import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sys
import time
import xml
import random

class Recommender(object):
    def __init__(self, training_set, test_set):
        if isinstance(training_set, str):
            # the training set is a file name
            self.training_set = pd.read_csv(training_set)
        else:
            # the training set is a DataFrame
            self.training_set = training_set.copy()

        if isinstance(test_set, str):
            # the test set is a file name
            self.test_set = pd.read_csv(test_set)
        else:
            # the test set is a DataFrame
            self.test_set = test_set.copy()
    
    def train_user_euclidean(self, data_set, userId):
        weights_euclidean = {}
        for user in data_set.columns[1:]:
            #print(user)
            if user != userId:
                df_subset = data_set[[userId, user]][data_set[userId].notnull() & data_set[user].notnull()]
                if df_subset.empty:
                    weights_euclidean[user] = 0
                else:
                    dist = euclidean(df_subset[userId], df_subset[user])
                    weights_euclidean[user] = 1.0 / (1.0 + dist)
        # print("start test print\neuclidean weights:")
        # print(weights_euclidean)
        # print("end test print")

        return weights_euclidean # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}
    
    def train_user_manhattan(self, data_set, userId):
        weights_manhattan = {}
        for user in data_set.columns[1:]:
            if user != userId:
                df_subset = data_set[[userId, user]][data_set[userId].notnull() & data_set[user].notnull()]
                dist = cityblock(df_subset[userId],df_subset[user])
                weights_manhattan[user] = 1.0 / (1.0 + dist)
        # print("start test print\nmanhattan weights:")
        # print(weights_manhattan)
        # print("end test print")
        return weights_manhattan # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

    def train_user_cosine(self, data_set, userId):
        weights_cosine = {}
        for user in data_set.columns[1:]:
            if user != userId:
                df_subset = data_set[[userId, user]][data_set[userId].notnull() & data_set[user].notnull()]
                if df_subset.empty:
                    weights_cosine[user] = 0
                else:
                    weights_cosine[user] = cosine(df_subset[userId], df_subset[user])
        # print("start test print\ncosine weights:")
        # print(weights_cosine)
        # print("end test print")
        return weights_cosine # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}
   
    def train_user_pearson(self, data_set, userId):
        weights_pearson = {}
        for user in data_set.columns[1:]:
            if user != userId:
                df_subset = data_set[[userId, user]][data_set[userId].notnull() & data_set[user].notnull()]
                if df_subset.empty:
                    weights_pearson[user] = 0
                else:
                    weight = pearsonr(df_subset[userId], df_subset[user])[0]
                    weights_pearson[user] = weight
        return weights_pearson # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

    def train_user(self, data_set, distance_function, userId):
        if distance_function == 'euclidean':
            return self.train_user_euclidean(data_set, userId)
        elif distance_function == 'manhattan':
            return self.train_user_manhattan(data_set, userId)
        elif distance_function == 'cosine':
            return self.train_user_cosine(data_set, userId)
        elif distance_function == 'pearson':
            return self.train_user_pearson(data_set, userId)
        else:
            return None

    def get_user_existing_ratings(self, data_set, userId):
        existing_ratings = []
        df_subset = data_set[['movieId',userId]].copy()
        for row in df_subset.itertuples(index=False):
            if not np.isnan(row[1]):
                existing_ratings.append((row[0],row[1]))
        return existing_ratings # list of tuples with movieId and rating. e.g. [(32, 4.0), (50, 4.0)]

    def predict_user_existing_ratings_top_k(self, data_set, sim_weights, userId, k):
        prediction = []
        list = sorted(sim_weights.items(), key=lambda item: item[1], reverse=True)
        list = dict(list[:k])
        #print(list)
        for index, row in data_set.iterrows():
            if not np.isnan(row[userId]):
                predicted_rating = 0.0
                weights_sum = 0.0
                ratings = data_set.iloc[index][1:]
                #print(list)
                #print(ratings)
                for user in data_set.columns[1:]:
                    if user != userId:
                        if (not np.isnan(ratings[user]) and user in list.keys()):
                            if (not np.isnan(list[user])):
                                predicted_rating += ratings[user] * list[user]
                                weights_sum += list[user]
                #print(predicted_rating)
                #print(weights_sum)
                if weights_sum == 0:
                    continue
                else:
                    predicted_rating /= weights_sum
                    r = (int(row[0]), predicted_rating)
                prediction.append(r)
        return prediction # list of tuples with movieId and rating. e.g. [(32, 4.0), (50, 4.0)]
    
    def evaluate(self, existing_ratings, predicted_ratings):
        existing_copy  = []
        predicted_copy = []
        existing_key   = []
        predicted_key  = []

        for i in existing_ratings:
            if not np.isnan(i[1]):
                existing_key.append(i[0])
        for i in predicted_ratings:
            if not np.isnan(i[1]):
                predicted_key.append(i[0])
        intersection = list(set(existing_key) & set(predicted_key))

        for key in intersection:
            for tuple in existing_ratings:
                if tuple[0] == key:
                    #print('exist')
                    #print(tuple)
                    existing_copy.append(tuple)
            for tuple in predicted_ratings:
                if tuple[0] == key:
                    #print('predict')
                    #print(tuple)
                    predicted_copy.append(tuple)
        #rmse
        exist_ratings = []
        predict_ratings = []
        for i in existing_copy:
            #print('existing copy')
            #print(i[1])
            exist_ratings.append(i[1])
        for i in predicted_copy:
            #print('predicted copy')
            #print(i[1])
            predict_ratings.append(i[1])
        rmse = np.sqrt(((np.array(predict_ratings) - np.array(exist_ratings)) ** 2).mean())

        #ratio
        exist_num = len(existing_key)
        #print(exist_num)
        inter_num = len(intersection)
        #print(inter_num)
        ratio = inter_num/exist_num
        return {'rmse':rmse, 'ratio':ratio} # dictionary with an rmse value and a ratio. e.g. {'rmse':1.2, 'ratio':0.5}
    
    def single_calculation(self, distance_function, userId, k_values):
        user_existing_ratings = self.get_user_existing_ratings(self.test_set, userId)
        print("User has {} existing and {} missing movie ratings".format(len(user_existing_ratings), len(self.test_set) - len(user_existing_ratings)), file=sys.stderr)

        print('Building weights')
        sim_weights = self.train_user(self.training_set[self.test_set.columns.values.tolist()], distance_function, userId)

        result = []
        for k in k_values:
            print('Calculating top-k user prediction with k={}'.format(k))
            top_k_existing_ratings_prediction = self.predict_user_existing_ratings_top_k(self.test_set, sim_weights, userId, k)
            result.append((k, self.evaluate(user_existing_ratings, top_k_existing_ratings_prediction)))
        return result # list of tuples, each of which has the k value and the result of the evaluation. e.g. [(1, {'rmse':1.2, 'ratio':0.5}), (2, {'rmse':1.0, 'ratio':0.9})]

    def aggregate_calculation(self, distance_functions, userId, k_values):
        print()
        result_per_k = {}
        for func in distance_functions:
            print("Calculating for {} distance metric".format(func))
            for calc in self.single_calculation(func, userId, k_values):
                if calc[0] not in result_per_k:
                    result_per_k[calc[0]] = {}
                result_per_k[calc[0]]['{}_rmse'.format(func)] = calc[1]['rmse']
                result_per_k[calc[0]]['{}_ratio'.format(func)] = calc[1]['ratio']
            print()
        result = []
        for k in k_values:
            row = {'k':k}
            row.update(result_per_k[k])
            result.append(row)
        columns = ['k']
        for func in distance_functions:
            columns.append('{}_rmse'.format(func))
            columns.append('{}_ratio'.format(func))
        result = pd.DataFrame(result, columns=columns)
        return result
        
if __name__ == "__main__":
    recommender = Recommender("data/train.csv", "data/small_test.csv")
    print("Training set has {} users and {} movies".format(len(recommender.training_set.columns[1:]), len(recommender.training_set)))
    print("Testing set has {} users and {} movies".format(len(recommender.test_set.columns[1:]), len(recommender.test_set)))

    result = recommender.aggregate_calculation(['euclidean', 'cosine', 'pearson', 'manhattan'], "0331949b45", [1, 2, 3, 4])
    print(result)