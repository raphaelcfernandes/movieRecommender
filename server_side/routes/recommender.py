from surprise import Dataset, Reader
from surprise import SVD
from operator import itemgetter
import pandas as pd
import os,time,re,sys,json

myMovies = []
movieListFromAngular = json.loads(sys.argv[1])
for i in movieListFromAngular:
	myDict = {"userId":999999,"movieId":i.get("movieId"),"rating":i.get("rating")}
	myMovies.append(myDict)
del myDict

testDataFrame = pd.DataFrame(myMovies)
testDataFrame = testDataFrame[['userId','movieId','rating']]
testDataFrame.rating = testDataFrame.rating.astype('float32')
testDataFrame.userId = testDataFrame.userId.astype('int32')
testDataFrame.movieId = testDataFrame.movieId.astype('int32')
user_id = 999999

ratings = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/ml-latest-small/ratings.csv",usecols=['userId', 'movieId', 'rating'])
ratings = ratings.append(testDataFrame,ignore_index=True)

movies = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/ml-latest-small/movies.csv")
   
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

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
finalResult = []
for index, i in enumerate(t[-10:]):
    # finalResult.append((movies[movies.movieId == i[1]][['title', 'genres']].values[0][0],movies[movies.movieId == i[1]][['title', 'genres']].values[0][1]),)
	finalResult.append(movies[movies.movieId == i[1]]['title'].values[0])
print(json.dumps(finalResult))
sys.stdout.flush()