from surprise import Dataset, Reader
from surprise import SVD
from operator import itemgetter
import pandas as pd
import os,time,re,sys,json

myMovies = []
movieListFromAngular = json.loads(sys.argv[1])
# movieListFromAngular = [{"movieId":69122,"rating":4}, #Matrix revolutions
# 	{"movieId":86911,"rating":4}, #matrix reloaded
# 	{"movieId":54503,"rating":3}, #Iron man
# 	{"movieId":52973,"rating":4}, #Iron man 2
# 	{"movieId":8807,"rating":4}, #Iron man 3
# 	{"movieId":3617,"rating":4}, #Deadpool
# 	{"movieId":35836,"rating":3}, #Interstellar
# 	{"movieId":2706,"rating":5}, #Fast and furious
# 	{"movieId":111362,"rating":5}, # xmen future past
# 	{"movieId":168252,"rating":5}] #Long
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

# Filter sparse users
min_user_ratings = 200 #Good one
filter_users = (ratings['userId'].value_counts() > min_user_ratings)
filter_users = filter_users[filter_users].index.tolist()

ratings = ratings[(ratings['movieId'].isin(filter_movies)) & (ratings['userId'].isin(filter_users))]

ratings = ratings.append(testDataFrame,ignore_index=True)
ratings.rating = ratings.rating.astype('float32')
ratings.userId = ratings.userId.astype('int32')
ratings.movieId = ratings.movieId.astype('int32')

movies = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/ml-latest/movies.csv")
movies = movies[movies.movieId.isin(filter_movies)]
del filter_movies, filter_users

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

algo = SVD()
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
    # finalResult.append((movies[movies.movieId == i[1]][['title', 'genres']].values[0][0],movies[movies.movieId == i[1]][['title', 'genres']].values[0][1]),)
	# finalResult.append({movies[movies.movieId == i[1]]['title'].values[0]:movies[movies.movieId == i[1]]['genres'].values[0]})
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