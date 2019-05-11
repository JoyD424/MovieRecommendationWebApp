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
    
    print(ratingsList[10]) # TEST 

    ratingsDF = pd.DataFrame(ratingsList, columns = ratingsColumnNames, dtype = int)
    return ratingsDF


# Create pivoted DF from data from DB
# Rows: UserID, Columns: MovieID of every movie in MovieLens database
# Table fill values: rating (int) of userID for movieID
# -> DataFrame
def getPivotedDataFrame():
    pivotedDF = getRatingDFFromDB()
    pivotedDF = pivotedDF.pivot(index='userID', columns='movieID', values='rating').fillna(0)
    return pivotedDF


# Create DF for movies from MovieLens database (use for initial data dump)
# -> DataFrame
def getMovieDFFromDB():
    allMovies = Movie.objects.all()

    moviesColumnNames = ['movieID', 'title', 'genres']
    moviesList = []
    
    for movie in allMovies:
        newMovie = [str(movie.movieID), str(movie.movieTitle), str(movie.movieGenres)]
        moviesList.append(newMovie)
    
    print(moviesList[:5]) # TEST

    moviesDF = pd.DataFrame(moviesList, columns = moviesColumnNames, dtype = int)

    return moviesDF