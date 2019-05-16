from django.contrib.auth.models import User
from .models import Movie, Rating, RecommendationHistory
from django.shortcuts import render, get_object_or_404, redirect
import string

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

    """print(dict)
    print(movie.movieID for movie in listMovie)"""
    return listMovie