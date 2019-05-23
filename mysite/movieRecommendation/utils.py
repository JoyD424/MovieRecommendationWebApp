from django.contrib.auth.models import User
from .models import Movie, Rating, RecommendationHistory
from django.shortcuts import render, get_object_or_404, redirect
from .TMDB_API import getMovieImageURLs
import string



# Check if a user has rated any movies
# Int -> Bool
def hasRatedMovies(userID):
    if Rating.objects.filter(userID = userID):
        return True
    return False


# Check if a movie object has assigned poster and backdrop urls.
# If not, assign them and return the urls.
# Movie -> 
def assignImageURLs(movie):
    if movie.moviePosterURL == '' and movie.movieBackdropURL == '':
        posterURL, backdropURl = getMovieImageURLs(movie.movieTitle)
        movie.moviePosterURL = posterURL
        movie.movieBackdropURL = backdropURl
        movie.save()
    
    else:
        print("error")

    return



# Check if a RecommendationHistory object already exists
def alreadyHasRecHistory(userID):
    try:
        obj = RecommendationHistory.objects.get(userID = userID)
    except RecommendationHistory.DoesNotExist:
        return False
    return True


# Convert RecommendationHistory.recommendations to a list
# Ex: "1,2,4,23" -> [1, 2, 4, 23]
def convertStrToLst(str):
    mappedObj = map(int, str.split(","))
    try:
        listInt = list(mappedObj)
    except TypeError:
        listInt = []
        print("TypeError")
    return listInt


# Convert list int to string for RecommendationHistory.recommendations
def convertLstToStr(listInt):
    string = ",".join(str(i) for i in listInt)
    return string


# List (Int, Int), Dict -> List Movie
def getMoviesList(listTuple, dict):
    listMovie = []
    for tuple in listTuple:
        movie = get_object_or_404(Movie, movieID = tuple[0])
        listMovie.append(movie)
        if movie.movieID not in dict.keys():
            dict[movie.movieID] = tuple[1]

    return listMovie



# List Int -> List Movie
def getPredMoviesList(listID):
    listMovie = []
    for id in listID:
        movie = get_object_or_404(Movie, movieID = id)
        listMovie.append(movie)

    return listMovie