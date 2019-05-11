import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from .databaseToDataframe import getMovieDFFromDB, getRatingDFFromDB, getPivotedDataFrame
import sys

""" References:
https://www.analyticsvidhya.com/blog/2018/06/comprehensive-guide-recommendation-engine-python/
https://beckernick.github.io/matrix-factorization-recommender/
"""

""" Example:
    ratingsDF = getRatingDataFrame()
    moviesDF = getMovieDataFrame()
    pivotedRatingsDF = getPivotedDataFrame()
    predictionsDF = getMoviePredictionDataframe(pivotedRatingsDF)
    alreadyRatedList, predictionsList = getRecommendations(predictionsDF, 837, moviesDF, ratingsDF, 10)
"""

# Int, Int -> List (Int, Int), List (Int, int)
def runRecEngine(userID, numRecommendations=10):

    moviesDF = getMovieDFFromDB()
    pivotedRatingsDF = getPivotedDataFrame()
    predictionsDF = getMoviePredictionDataframe(pivotedRatingsDF)
    alreadyRatedList, predictionsList = getRecommendations(predictionsDF, userID, moviesDF, pivotedRatingsDF, numRecommendations)

    return alreadyRatedList, predictionsList



# Get movie recommendations for a specific user
# Returns a list of already rated movies (as tuple, where (movieID, rating))
# Also returns a list of predicted movies that user will like as a tuple where (movieID, predictedRating)
# DF, int, DF, DF, Int -> List (Int, Int), List (Int, Int)
def getRecommendations(predictionsDF, userID, moviesDF, originalPivotedRatingsDF, numRecommendations):
    
    # Get the movies that the user had rated already 
    alreadyRatedData = originalPivotedRatingsDF.iloc[[userID - 1]] 
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


# Get prediction dataframe of the ratings of movies each user might give
# -> DataFrame
def getMoviePredictionDataframe(pivotedRatingsDF):
    # Turn pivotedRatingsDF into a matrix
    ratingsMatrix  = pivotedRatingsDF.as_matrix()

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
    predictionsDF = pd.DataFrame(predictedRatingsMatrix, columns = pivotedRatingsDF.columns)
    
    return predictionsDF