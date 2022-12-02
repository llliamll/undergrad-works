import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Task(object):
    def __init__(self, data):
        self.df = pd.read_csv(data)

    def t1(self, name):
        sim_weights = {}
        for user in self.df.columns[1:]:
            if user != name:
                df_subset = self.df[[name, user]][self.df[name].notnull() & self.df[user].notnull()]
                if df_subset.empty:
                    sim_weights[user] = 0
                else:
                    sim_weights[user] = cosine(df_subset[name], df_subset[user])

        # print("similarity weights: %s" % sim_weights)
        result = []

        for index, row in self.df.iterrows():
            if np.isnan(row[name]):
                predicted_rating = 0.0
                weights_sum = 0.0
                ratings = self.df.iloc[index][1:]
                for user in self.df.columns[1:]:
                    if (user != name):
                        if (not np.isnan(ratings[user])):
                            predicted_rating += ratings[user] * sim_weights[user]
                            weights_sum += sim_weights[user]
                predicted_rating /= weights_sum
                r = (row[0], predicted_rating)
                result.append(r)
        return result

    def t2(self, name):
        df1 = self.df.set_index('Alias').T
        #print(df1.loc[name])
        sim_weights = {}
        df_nan = []
        df_notNan = []
        for movies in df1.loc[name]:
            if movies != None:
                if np.isnan(movies):
                    for rated_movies in df1.loc[name]:
                        sim_weights[movies] = cosine(movies, rated_movies)
        #print(sim_weights)


    def t3(self, name):
        sim_weights = {}
        temp = {}
        for user in self.df.columns[1:]:
            if user != name:
                df_subset = self.df[[name, user]][self.df[name].notnull() & self.df[user].notnull()]
                if df_subset.empty:
                    temp[user] = 0
                else:
                    temp[user] = cosine(df_subset[name], df_subset[user])
        # print("similarity weights: %s" % sim_weights)

        list = sorted(temp.items(), key=lambda item: item[1], reverse=True)
        list = dict(list[:10])
        # print(sim_weights)

        result = []
        for index, row in self.df.iterrows():
            if np.isnan(row[name]):
                predicted_rating = 0.0
                weights_sum = 0.0
                ratings = self.df.iloc[index][1:]
                for user in self.df.columns[1:]:
                    if (user != name):
                        if (not np.isnan(ratings[user]) and user in list.keys()):
                            predicted_rating += ratings[user] * list[user]
                            weights_sum += list[user]
                predicted_rating /= weights_sum
                r = (row[0], predicted_rating)
                result.append(r)
        return result


if __name__ == "__main__":
    # using the class movie ratings data we collected in http://data.cs1656.org/movie_class_responses.csv
    t = Task('http://data.cs1656.org/movie_class_responses.csv')
    print(t.t1('BabyKangaroo'))
    print('------------------------------------')
    print(t.t2('BabyKangaroo'))
    print('------------------------------------')
    print(t.t3('BabyKangaroo'))
    print('------------------------------------')