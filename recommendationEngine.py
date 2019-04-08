import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import sys

""" Source:
https://beckernick.github.io/matrix-factorization-recommender/
"""

""" Example:
    ratingsDF = getRatingDataFrame()
    moviesDF = getMovieDataFrame()
    predictionsDF = getMoviePredictionDataframe(ratingsDF)
    alreadyRatedList, predictionsList = getRecommendations(predictionsDF, 837, moviesDF, ratingsDF, 10)
"""


# Get movie recommendations for a specific user
# -> List (Int, Int), List (Int, Int)
def getRecommendations(predictionsDF, userID, moviesDF, originalRatingsDF, numRecommendations=10):
    
    # Get the movies that the user had rated already 
    alreadyRatedData = originalRatingsDF.iloc[[userID - 1]] 
    print(alreadyRatedData) # TEST
    columns = list(alreadyRatedData)
    alreadyRatedMovies = [] # List (Int, Int) of movieID, rating tuple
    for movieID in columns:
        rating = int(alreadyRatedData.loc[userID, movieID])
        if rating != 0:
            alreadyRatedMovies.append((movieID, rating))

    # Get movie recommendations for movies the user hasn't seen yet
    userPrediction = predictionsDF.iloc[[userID]]
    print(userPrediction)
    columns = list(userPrediction)
    predictionsList = [] # List (Int, Int) of movieID, rating tuple
    for movieID in columns:
        predictedRating = int(userPrediction.loc[userID, movieID])
        if predictedRating != 0 and not inList(alreadyRatedMovies, movieID):
            if predictedRating >= 3:
                predictionsList.append((movieID, predictedRating))
    predictionsList.sort(key = lambda x: x[1], reverse = True)

    # Check to make sure the number of predictions is less than or equal to 
    # the number of user requested recommendations
    numRecommendations = checkPredictionListSize(predictionsList, numRecommendations)

    return alreadyRatedMovies, predictionsList[:numRecommendations]


# Checks to make sure length of predictions is equal to or longer than 
# the requested amount of recommendations. If not, return the length
# of the predictions
# List (Int, Int), Int -> Int
def checkPredictionListSize(predictionsList, numRecommendations):
    lenPredictions = len(predictionsList)
    if lenPredictions < numRecommendations:
        numRecommendations = lenPredictions

    return numRecommendations


# Check if an integer value is in a list
# List (Int, Int), Int -> Bool
def inList(list, val):
    dict = {i : j for i, j in list}
    if val in dict:
        return True
    return False


# Create DF for ratings from MovieLens database
# -> DataFrame
def getRatingDataFrame():
    data = open('/Users/joyding/Documents/movie_recommender/ml-1m/ratings.dat', 'r')
    ratingsList = [line.strip().split("::") for line in data.readlines()]
    ratingColumnNames = ['userID', 'movieID', 'rating', 'timeStamp']
    ratingsDF = pd.DataFrame(ratingsList, columns = ratingColumnNames, dtype = int)
    ratingsDF = ratingsDF.pivot(index='userID', columns='movieID', values='rating').fillna(0)
    return ratingsDF


# Create DF for movies from MovieLens database
# -> DataFrame
def getMovieDataFrame():
    data = open('/Users/joyding/Documents/movie_recommender/ml-1m/movies.dat', 'r', encoding = "latin-1")
    moviesList = [line.strip().split("::") for line in data.readlines()]
    movieColumnNames = ['movieID', 'title', 'genres']
    moviesDF = pd.DataFrame(moviesList, columns = movieColumnNames)
    moviesDF['movieID'] = moviesDF['movieID'].apply(pd.to_numeric)
    return moviesDF


# Get prediction dataframe of the ratings of movies each user might give
# -> DataFrame
def getMoviePredictionDataframe(ratingsDF):
    # Turn ratingsDF into a matrix
    ratingsMatrix  = ratingsDF.as_matrix()

    # Demean (normalize by each user mean) data
    userMeanRatings = np.mean(ratingsMatrix, axis = 1)
    demeanedRatingsMatrix = ratingsMatrix - userMeanRatings.reshape(-1, 1)

    # Perform singular value decomposition
    U, sigma, Vt = svds(demeanedRatingsMatrix, k = 50)

    # Convert to diagonal matrix form
    sigma = np.diag(sigma)

    # Predictions as matrix
    predictedRatingsMatrix = np.dot(np.dot(U, sigma), Vt) + userMeanRatings.reshape(-1, 1)

    # Predictions for all users as Data Frame
    predictionsDF = pd.DataFrame(predictedRatingsMatrix, columns = ratingsDF.columns)
    
    return predictionsDF