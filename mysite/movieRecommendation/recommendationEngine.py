import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from .databaseToDataframe import getMovieDFFromDB, getRatingDFFromDB, getPivotedDataFrame #, getRatingDataFrame, getMovieDataFrame, getPivotedDataFrame2
import sys



""" References:
https://medium.com/@paritosh_30025/recommendation-using-matrix-factorization-5223a8ee1f4
https://www.analyticsvidhya.com/blog/2018/06/comprehensive-guide-recommendation-engine-python/
https://towardsdatascience.com/how-to-build-a-simple-recommender-system-in-python-375093c3fb7d
https://beckernick.github.io/matrix-factorization-recommender/
https://machinelearningmastery.com/introduction-to-matrix-decompositions-for-machine-learning/
"""



# Int, Int -> List (Int, Int), List (Int, int)
def runRecEngine(userID): #, numRecommendations=10):
    moviesDF = getMovieDFFromDB()
    pivotedRatingsDF = getPivotedDataFrame()
    predictionsDF = getMoviePredictionDataframe(pivotedRatingsDF)
    alreadyRatedList, predictionsList = getRecommendations(predictionsDF, userID, moviesDF, pivotedRatingsDF) #, numRecommendations)

    return alreadyRatedList, predictionsList



# This function is for .views file (similar to getAlreadyRatedList)
def getAlreadyRated(userID):
    pivotedRatingsDF = getPivotedDataFrame()
    result = getAlreadyRatedList(userID, pivotedRatingsDF)
    return result



# DF -> List (Int, Int)
def getAlreadyRatedList(userID, originalPivotedRatingsDF):
    try:
        index = list(originalPivotedRatingsDF.index.values)[userID - 1]
        alreadyRatedData = originalPivotedRatingsDF.loc[[index], : ] 
    except IndexError:
        # If the user has not rated any movies
        print("Index Error")
        return []
    columns = list(alreadyRatedData)
    index = list(alreadyRatedData.index.values)[0]
    alreadyRatedMovies = [] # List (Int, Int) of movieID, rating tuple
    for movieID in columns:
        rating = int(alreadyRatedData.loc[index, movieID])
        if rating != 0:
            alreadyRatedMovies.append((movieID, rating))
    return alreadyRatedMovies



# Get movie recommendations for a specific user
# Returns a list of already rated movies (as tuple, where (movieID, rating))
# Also returns a list of predicted movies that user will like as a tuple where (movieID, predictedRating)
# DF, int, DF, DF, Int -> List (Int, Int), List (Int, Int)
def getRecommendations(predictionsDF, userID, moviesDF, originalPivotedRatingsDF): #, numRecommendations):
    # Get the movies that the user had rated already
    alreadyRatedMovies = getAlreadyRatedList(userID, originalPivotedRatingsDF)
    if alreadyRatedMovies == []:
        print("Hasn't rated any movies")
        return [], []
    # Get movie recommendations for movies the user hasn't seen yet
    newUserID = userID - 1
    userPrediction = predictionsDF.iloc[[newUserID], : ].sort_values(by=newUserID, axis=1, ascending=False)
    columns = list(userPrediction)
    predictionsList = [] # List (Int, Int) of movieID, rating tuple
    for movieID in columns:
        if not inList(alreadyRatedMovies, movieID): # and num <= numRecommendations:
            predictedRating = round(userPrediction[movieID][newUserID], 4) 
            predictionsList.append((movieID, predictedRating))
    predictionsList.sort(key = lambda x: x[1], reverse = True)

    return alreadyRatedMovies, predictionsList 



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