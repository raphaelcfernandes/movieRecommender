from surprise import Dataset, evaluate, Reader, dump
from surprise import SVD, SVDpp
from surprise.model_selection import cross_validate
from collections import deque,defaultdict
from surprise import KNNWithMeans
from operator import itemgetter
from pymongo import MongoClient
import pandas as pd
import numpy as np
import os,io,time,re,sys

#MOVIELENS
test = [{"userId":999999,"movieId":33794,"rating":5},
{"userId":999999,"movieId":68319,"rating":5},
{"userId":999999,"movieId":5952,"rating":5},
{"userId":999999,"movieId":4262,"rating":5},
{"userId":999999,"movieId":8644,"rating":5},
{"userId":999999,"movieId":2571,"rating":4},
{"userId":999999,"movieId":6016,"rating":5},
{"userId":999999,"movieId":318,"rating":5},
{"userId":999999,"movieId":858,"rating":5},
{"userId":999999,"movieId":19,"rating":4}]

testDataFrame = pd.DataFrame(test)
testDataFrame = testDataFrame[['userId','movieId','rating']]
testDataFrame.rating = testDataFrame.rating.astype('float32')
testDataFrame.userId = testDataFrame.userId.astype('int32')
testDataFrame.movieId = testDataFrame.movieId.astype('int32')
user_id = 999999

ratings = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/movielens20M/rating.csv",usecols=['userId', 'movieId', 'rating'])
ratings = ratings.append(testDataFrame,ignore_index=True)
#27278 movies
movies = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/movielens20M/movie.csv")
#Then load 100k movielens
   
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# print('###################### MOVIES SELECTED BY THE USER ###############################')
# for index, row in ratings.iterrows():
#     if(row.userId == user_id):
#         print(movies[movies.movieId == row.movieId]
#               [['title', 'genres']].values[0])
# print('#################### RECOMMENDATION ##################################################')
algo = SVD()
trainingSet = data.build_full_trainset()
algo.fit(trainingSet)
    
ids = pd.Series(ratings.movieId, name='movieId').unique()
x = ratings[(ratings.movieId.isin(ids)) & (ratings.userId != user_id)]

x = x[~x.movieId.isin(testDataFrame.movieId.values)] #id do testDataFrame

t = []
for rows in x.movieId.unique():
    t.append(algo.predict(user_id, rows))
t = sorted(t, key=itemgetter(3))
for index, i in enumerate(t[-10:]):
    print("Top #", index+1,
        movies[movies.movieId == i[1]][['title', 'genres']].values[0],i[3])
sys.stdout.flush()

# movies = pd.read_csv("movielens20M/movie.csv")

# client = MongoClient('localhost',27017)
# client.drop_database(client.movies)
# mydb = client.movies

# mydb.movies.drop()
# t = []
# for index,i in movies.iterrows():
#     t.append(i)
#     print(i)
#     try:
#         year = re.search(r'\((.*?)\)',i.title).group(1)
#     except:
#         year = 0
#     data = {
#         "movieId": int(i.movieId),
#         "year": year,
#         "title": i.title[:i.title.find("(")],
#         "genres": i.genres.split("|"),
#     }
#     mydb.movies.insert_one(data)
#     t = []