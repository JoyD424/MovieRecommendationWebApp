import pandas as pd
from .models import Movie, Rating

# Create DF from database information
# -> DataFrame
def getRatingDFFromDB():
    allRatings = Rating.objects.all()

    ratingsColumnNames = ['userID', 'movieID', 'rating']
    ratingsList = []
    
    for rating in allRatings:
        newRating = [str(rating.userID), str(rating.movieID), str(rating.rating)]
        ratingsList.append(newRating)

    ratingsDF = pd.DataFrame(ratingsList, columns = ratingsColumnNames, dtype = int)
    return ratingsDF

"""# Create DF for ratings from MovieLens database
# -> DataFrame
def getRatingDataFrame():
    data = open('/Users/joyding/Documents/movie_recommender/ml-1m/ratings.dat', 'r')
    ratingsList = [line.strip().split("::") for line in data.readlines()]
    ratingColumnNames = ['userID', 'movieID', 'rating', 'timeStamp']
    ratingsDF = pd.DataFrame(ratingsList, columns = ratingColumnNames, dtype = int)
    return ratingsDF

# Create DF for movies from MovieLens database
# -> DataFrame
def getMovieDataFrame():
    data = open('/Users/joyding/Documents/movie_recommender/ml-1m/movies.dat', 'r', encoding = "latin-1")
    moviesList = [line.strip().split("::") for line in data.readlines()]
    movieColumnNames = ['movieID', 'title', 'genres']
    moviesDF = pd.DataFrame(moviesList, columns = movieColumnNames)
    moviesDF['movieID'] = moviesDF['movieID'].apply(pd.to_numeric)
    return moviesDF"""


# Create pivoted DF from data from DB
# Rows: UserID, Columns: MovieID of every movie in MovieLens database
# Table fill values: rating (int) of userID for movieID
# -> DataFrame
def getPivotedDataFrame():
    pivotedDF = getRatingDFFromDB()
    pivotedDF = pivotedDF.pivot(index='userID', columns='movieID', values='rating').fillna(0)
    return pivotedDF


"""# Create pivoted DF from data from DB
# Rows: UserID, Columns: MovieID of every movie in MovieLens database
# Table fill values: rating (int) of userID for movieID
# -> DataFrame
def getPivotedDataFrame2():
    pivotedDF = getRatingDataFrame()
    pivotedDF = pivotedDF.pivot(index='userID', columns='movieID', values='rating').fillna(0)
    return pivotedDF"""


# Create DF for movies from MovieLens database (use for initial data dump)
# -> DataFrame
def getMovieDFFromDB():
    allMovies = Movie.objects.all()

    moviesColumnNames = ['movieID', 'title', 'genres']
    moviesList = []
    
    for movie in allMovies:
        newMovie = [str(movie.movieID), str(movie.movieTitle), str(movie.movieGenres)]
        moviesList.append(newMovie)

    moviesDF = pd.DataFrame(moviesList, columns = moviesColumnNames, dtype = int)

    return moviesDF