import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from .databaseToDataframe import getMovieDFFromDB, getRatingDFFromDB, getPivotedDataFrame #, getRatingDataFrame, getMovieDataFrame, getPivotedDataFrame2
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
    # movies2DF = getMovieDataFrame()

    pivotedRatingsDF = getPivotedDataFrame()
    print(pivotedRatingsDF)
    """pivotedRatingsDF2 = getPivotedDataFrame2()
    print(pivotedRatingsDF)
    print(pivotedRatingsDF2)"""

    predictionsDF = getMoviePredictionDataframe(pivotedRatingsDF)
    """predictionsDF2 = getMoviePredictionDataframe(pivotedRatingsDF2)
    print(predictionsDF.equals(predictionsDF2))"""
    print(predictionsDF)
    # print(predictionsDF2)
    alreadyRatedList, predictionsList = getRecommendations(predictionsDF, userID, moviesDF, pivotedRatingsDF, numRecommendations)
    # alreadyRatedList2, predictionsList2 = getRecommendations(predictionsDF2, userID, movies2DF, pivotedRatingsDF2, numRecommendations)

    return alreadyRatedList, predictionsList



# This function is for .views file (similar to getAlreadyRatedList)
def getAlreadyRated(userID):
    pivotedRatingsDF = getPivotedDataFrame()
    result = getAlreadyRatedList(userID, pivotedRatingsDF)
    return result



# DF -> List (Int, Int)
def getAlreadyRatedList(userID, originalPivotedRatingsDF):
    try:
        print(userID)
        alreadyRatedData = originalPivotedRatingsDF.iloc[[userID - 1], : ] 
        print(alreadyRatedData)
    except IndexError:
        # If the user has not rated any movies
        return [], []
    columns = list(alreadyRatedData)
    alreadyRatedMovies = [] # List (Int, Int) of movieID, rating tuple
    for movieID in columns:
        rating = int(alreadyRatedData.loc[userID, movieID])
        if rating != 0:
            alreadyRatedMovies.append((movieID, rating))
    return alreadyRatedMovies



# Get movie recommendations for a specific user
# Returns a list of already rated movies (as tuple, where (movieID, rating))
# Also returns a list of predicted movies that user will like as a tuple where (movieID, predictedRating)
# DF, int, DF, DF, Int -> List (Int, Int), List (Int, Int)
def getRecommendations(predictionsDF, userID, moviesDF, originalPivotedRatingsDF, numRecommendations):
    # Get the movies that the user had rated already
    """print(userID)
    print(originalPivotedRatingsDF)
    print(predictionsDF)
    print(originalPivotedRatingsDF.iloc[[userID]]) # TEST
    print(predictionsDF.iloc[[userID - 1]]) # TESt"""
    alreadyRatedMovies = getAlreadyRatedList(userID, originalPivotedRatingsDF)
    """try:
        print(userID)
        alreadyRatedData = originalPivotedRatingsDF.iloc[[userID - 1], : ] 
        print(alreadyRatedData)
    except IndexError:
        # If the user has not rated any movies
        return [], []
    columns = list(alreadyRatedData)
    alreadyRatedMovies = [] # List (Int, Int) of movieID, rating tuple
    for movieID in columns:
        rating = int(alreadyRatedData.loc[userID, movieID])
        if rating != 0:
            alreadyRatedMovies.append((movieID, rating))"""

    # Get movie recommendations for movies the user hasn't seen yet
    newUserID = userID - 1
    userPrediction = predictionsDF.iloc[[newUserID], : ].sort_values(by=newUserID, axis=1, ascending=False)
    # print(userPrediction) # TEST
    # print(alreadyRatedMovies) # TEST
    columns = list(userPrediction)
    predictionsList = [] # List (Int, Int) of movieID, rating tuple
    num = 1
    for movieID in columns:
        if not inList(alreadyRatedMovies, movieID) and num <= numRecommendations:
            # print("Ok")
            predictedRating = round(userPrediction[movieID][newUserID], 4) # int(userPrediction.loc[userID - 1, movieID])
            predictionsList.append((movieID, predictedRating))
            num += 1
    predictionsList.sort(key = lambda x: x[1], reverse = True)

    # Check to make sure the number of predictions is less than or equal to 
    # the number of user requested recommendations

    print("Original numRec:", numRecommendations)
    print(len(predictionsList))
    print(predictionsList)
    # numRecommendations = checkPredictionListSize(predictionsList, numRecommendations)

    return alreadyRatedMovies, predictionsList # predictionsList[:numRecommendations]



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
    if val in dict.keys():
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