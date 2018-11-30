from pymongo import MongoClient
import os,re,sys
import pandas as pd


if sys.argv[1] == '100k':
    movies = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/ml-latest-small/movies.csv")
else:
    movies = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"/ml-latest/movies.csv")

client = MongoClient('localhost',27017)
client.drop_database(client.movies)
mydb = client.movies

mydb.movies.drop()
for index,i in movies.iterrows():
    try:
        year = re.search(r'\((.*?)\)',i.title).group(1)
    except:
        year = 0
    data = {
        "movieId": int(i.movieId),
        "year": year,
        "title": i.title[:i.title.find("(")],
        "genres": i.genres.split("|"),
    }
    mydb.movies.insert_one(data)