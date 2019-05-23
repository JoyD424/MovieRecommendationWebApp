from .config import api_key
import re
import requests
import time
import io



# Queries the API using a keyword search consisting of title.
# Sort response based on year of film release for the correct movie,
# And get that movie's poster url and backdrop url
# String -> String, String
def getMovieImageURLs(keywordSearch):
    titleList, year = convertToKeywordQuery(keywordSearch)
    titleQuery = "+".join(titleList)
    requestURL = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&query=" + titleQuery
    response = requests.get(requestURL)
    response = response.json()
    try:
        response['results']
    except KeyError:
        print(response)

    for movieData in response['results']:
        movieYear = convertDateToYear(movieData['release_date'])
        if movieYear == year:
            posterURL = movieData['poster_path']
            backdropURL = movieData['backdrop_path']
            if posterURL == None:
                posterURL = ''
            if backdropURL == None:
                backdropURL = ''
            """print(posterURL)
            print(backdropURL)"""
            return posterURL, backdropURL

    try:
        posterURL, backdropURL = response['results'][0]['poster_path'], response['results'][0]['backdrop_path']
        if posterURL == None:
                posterURL = ''
        if backdropURL == None:
            backdropURL = ''
        """print(posterURL)
        print(backdropURL)"""
        return posterURL, backdropURL
    except IndexError:
        print("Error! Empty search results for", titleList)
    
    return '', ''



# Convert a full date to a year
# Ex: "1994-05-07" -> "1994"
# String -> String
def convertDateToYear(fullDateStr):
    parsedDate = fullDateStr.split("-")
    year = parsedDate[0]
    return year



# Convert a title into a list of words and the date
# Ex: "Lion King, The (1994)" -> ["Lion", "King", "The"], "1994"
# String -> List String, String
def convertToKeywordQuery(keywordSearch):
    keywordSearch = re.sub(r'\(\D*?\)', '', keywordSearch)
    parsedList = keywordSearch.split()
    titleList = parsedList[:-1]
    date = parsedList[-1][1:-1]
    return titleList, date


def readDat():
    f = io.open('movies.dat', 'r')
    moviesLst = [line.strip().split("::") for line in f.readlines()]
    return moviesLst


def writeURLs(moviesLst):
    f = io.open('urls.txt', 'w', encoding='latin1')
    count = 0
    for movie in moviesLst:
        id = movie[0]
        title = movie[1]
        posterURL, backdropURL = getMovieImageURLs(title)
        try:
            str = id + '::' + posterURL + '::' + backdropURL
        except TypeError:
            print("error:", posterURL, backdropURL)
        f.write(str + '\n')
        count += 1
        if count == 40:
            count = 0
            time.sleep(20)
    return 