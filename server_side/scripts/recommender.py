from surprise import Dataset, Reader
from surprise import SVD
from operator import itemgetter
import pandas as pd
import os,time,re,sys,json

myMovies = []
movieListFromAngular = json.loads(sys.argv[1])
# movieListFromAngular = [{"movieId":168252,"rating":5}, #Logan
# 	{"movieId":552,"rating":5}, #3 Musketeers
# 	{"movieId":1408,"rating":5}, #Last of the Mohicans
# 	{"movieId":2947,"rating":5}, #Goldfinger
# 	{"movieId":3578,"rating":5}, #Gladiator
# 	{"movieId":4262,"rating":4}, #Scarface
# 	{"movieId":4310,"rating":5}, #Pearl Harbor
# 	{"movieId":4367,"rating":3}, #Laracroft: Tomb Raider
# 	{"movieId":4369,"rating":4}, #Fast and Furious
# 	{"movieId":4643,"rating":5}, #Planet of the apes
# 	{"movieId":5445,"rating":3}, #Minority Report
# 	{"movieId":5459,"rating":4}, #Man in Black II
# 	{"movieId":5785,"rating":5}, #Jackass: The Movie
# 	{"movieId":6016,"rating":5}, #City of god
# 	{"movieId":58559,"rating":5}, #Dark Knight
# 	{"movieId":6365,"rating":5}, #Matrix Reloaded
# 	{"movieId":59784,"rating":5}, #Kung Fu Panda
# 	{"movieId":72998,"rating":5}, #Avatar
# 	{"movieId":89745,"rating":5}, #The Avengers
# 	{"movieId":103042,"rating":3}, #Man of Steel
# 	{"movieId":112175,"rating":5}, #How to train your dragon 2
# 	{"movieId":122904,"rating":5}, #Deadpool
# 	{"movieId":122918,"rating":3}, #Guardians of the galaxy 2
# 	{"movieId":122922,"rating":5}, #Dr. Strange
# 	{"movieId":364,"rating":5}, #Lion King
# 	{"movieId":1907,"rating":5}, #Mulan
# 	{"movieId":2687,"rating":5}, #Tarzan
# 	{"movieId":8961,"rating":5}] #Incredibles 
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

ratings = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/ml-latest/ratings.csv",usecols=['userId', 'movieId', 'rating'])

# Filter sparse movies
min_movie_ratings = 4000
max_movie_ratings = 50000
filter_movies = ((ratings['movieId'].value_counts() > min_movie_ratings) & (ratings['movieId'].value_counts() < max_movie_ratings) )
filter_movies = filter_movies[filter_movies].index.tolist()

# # Filter sparse users
# min_user_ratings = 200 #Good one
# filter_users = (ratings['userId'].value_counts() > min_user_ratings)
# filter_users = filter_users[filter_users].index.tolist()

# ratings = ratings[(ratings['movieId'].isin(filter_movies)) & (ratings['userId'].isin(filter_users))]
ratings = ratings[(ratings['movieId'].isin(filter_movies))]

ratings = ratings.append(testDataFrame,ignore_index=True)
ratings.rating = ratings.rating.astype('float32')
ratings.userId = ratings.userId.astype('int32')
ratings.movieId = ratings.movieId.astype('int32')

movies = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/ml-latest/movies.csv")
movies = movies[movies.movieId.isin(filter_movies)]
# del filter_movies, filter_users
del filter_movies

reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

algo = SVD(n_epochs=15,n_factors=50)
trainingSet = data.build_full_trainset()
algo.fit(trainingSet)
    
ids = pd.Series(ratings.movieId, name='movieId').unique()
x = ratings[(ratings.movieId.isin(ids)) & (ratings.userId != user_id)]

x = x[~x.movieId.isin(testDataFrame.movieId.values)] #id do testDataFrame
del ratings,ids

t = []
for rows in x.movieId.unique():
    t.append(algo.predict(user_id, rows))
t = sorted(t, key=itemgetter(3))
finalResult = []
for index, i in enumerate(t[-10:]):
#     # finalResult.append((movies[movies.movieId == i[1]][['title', 'genres']].values[0][0],movies[movies.movieId == i[1]][['title', 'genres']].values[0][1]),)
# 	# finalResult.append({movies[movies.movieId == i[1]]['title'].values[0]:movies[movies.movieId == i[1]]['genres'].values[0]})
	movie = ''
	movie = movies[movies.movieId == i[1]]['title'].values[0] + ' - '
	k = ''
	for m in movies[movies.movieId == i[1]]['genres'].values[0].split("|"):
		k+=m+', '
	k = k[:-2]
	movie+=k
	# finalResult.append(movies[movies.movieId == i[1]]['title'].values[0])
	finalResult.append(movie)
print(json.dumps(finalResult))
sys.stdout.flush()