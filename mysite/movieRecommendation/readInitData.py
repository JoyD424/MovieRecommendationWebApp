import pandas as pd


# Create DF for ratings from MovieLens database
# -> DataFrame
def getRatingDataFrame():
    data = open('/Users/joyding/Documents/movie_recommender/ml-1m/ratings.dat', 'r')
    ratingsList = [line.strip().split("::") for line in data.readlines()]
    ratingColumnNames = ['userID', 'movieID', 'rating', 'timeStamp']
    ratingsDF = pd.DataFrame(ratingsList, columns = ratingColumnNames, dtype = int)
    return ratingsDF


# Create pivoted DF
# Rows: UserID, Columns: MovieID of every movie in MovieLens database
# Table fill values: rating of userID for movieID
# -> DataFrame
def getPivotedDataFrame():
    pivotedDF = getRatingDataFrame()
    pivotedDF = pivotedDF.pivot(index='userID', columns='movieID', values='rating').fillna(0)
    return pivotedDF


# Create DF for movies from MovieLens database
# -> DataFrame
def getMovieDataFrame():
    data = open('/Users/joyding/Documents/movie_recommender/ml-1m/movies.dat', 'r', encoding = "latin-1")
    moviesList = [line.strip().split("::") for line in data.readlines()]
    movieColumnNames = ['movieID', 'title', 'genres']
    moviesDF = pd.DataFrame(moviesList, columns = movieColumnNames)
    moviesDF['movieID'] = moviesDF['movieID'].apply(pd.to_numeric)
    return moviesDF