from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import Movie, Rating, RecommendationHistory
from .recommendationEngine import runRecEngine, getAlreadyRated
from .helperFunctions import alreadyHasRecHistory, convertLstToStr, convertStrToLst, getMoviesList
from string import ascii_uppercase

# Global Variable
UPPERCASE_LETTERS = list(ascii_uppercase)


def homepage(request):

    if not request.user.is_authenticated:
        return redirect("logIn")

    user_id = request.user.id

    recHistory = get_object_or_404(RecommendationHistory, userID = user_id)

    # If .recommendations haven't been added to object yet
    if recHistory.recommendations == '':
        alreadyRatedList, predictionsList = runRecEngine(user_id)
        newPredictions = []
        for tuple in predictionsList:
            newPredictions.append(tuple[0])
        recHistory.recommendations = convertLstToStr(newPredictions)
        recHistory.save()
        movieRatingDict = {}
        alreadyRatedMovies = getMoviesList(alreadyRatedList, movieRatingDict)
        predictionsMovies = getMoviesList(predictionsList, movieRatingDict)
        return render(request, 'movieRecommendation/homepage.html', {'alreadyRatedMovies': alreadyRatedMovies, 'predictionsMovies': predictionsMovies, 'movieRatingDict': movieRatingDict})
    
    if request.method == "GET":
        numRecs = request.GET.get('numRecs')
        print("NumRecs:", numRecs)
        if numRecs is None:
            alreadyRatedList, predictionsList = runRecEngine(user_id)
            recHistory.recommendations = convertLstToStr(newPredictions)
            recHistory.save()
        else:
            alreadyRatedList, predictionsList = runRecEngine(user_id, int(numRecs))
        

    else:
        alreadyRatedList = getAlreadyRated(user_id)
        predictionsList = convertStrToLst(recHistory.recommendations)

    movieRatingDict = {}
    alreadyRatedMovies = getMoviesList(alreadyRatedList, movieRatingDict)
    predictionsMovies = getMoviesList(predictionsList, movieRatingDict)
    """alreadyRatedList, predictionsList = runRecEngine(user_id)
    alreadyRatedMovies, predictionsMovies = [], []
    movieRatingDict = {}"""

    """if len(alreadyRatedList) != 0 and len(predictionsList) != 0:

        for tuple in alreadyRatedList:
            movie = get_object_or_404(Movie, movieID = tuple[0])
            alreadyRatedMovies.append(movie)
            if movie.movieID not in movieRatingDict.keys():
                movieRatingDict[movie.movieID] = tuple[1]

        for tuple in predictionsList:
            movie = get_object_or_404(Movie, movieID = tuple[0])
            predictionsMovies.append(movie)
            if movie.movieID not in movieRatingDict.keys():
                movieRatingDict[movie.movieID] = tuple[1]"""

    return render(request, 'movieRecommendation/homepage.html', {'alreadyRatedMovies': alreadyRatedMovies, 'predictionsMovies': predictionsMovies, 'movieRatingDict': movieRatingDict})



def index(request):

    if not request.user.is_authenticated:
        return redirect("logIn")

    allMovies = Movie.objects.all()

    if request.method == 'GET':
        query = request.GET.get('q')
        
        if query is None:
            return render(request, 'movieRecommendation/index.html', {'upperLetters': UPPERCASE_LETTERS})

        if 'submitTitle' in request.GET:
            submitbutton = request.GET.get('submitTitle')
            lookups = Q(movieTitle__icontains=query)

        elif 'submitGenre' in request.GET:
            submitbutton = request.GET.get('submitTitle')
            lookups = Q(movieGenres__icontains=query)

        elif 'submitStartsWith' in request.GET:
            submitbutton = request.GET.get('submitStartsWith')
            lookups = Q(movieTitle__startswith=submitbutton)
            
        results= Movie.objects.filter(lookups).distinct()

        context={'results': results,
                'submitbutton': submitbutton,
                'upperLetters': UPPERCASE_LETTERS
                }

        return render(request, 'movieRecommendation/index.html', context)

    return render(request, 'movieRecommendation/index.html', {'results': allMovies, 'upperLetters': UPPERCASE_LETTERS})



def movieDetail(request, movie_id):

    if not request.user.is_authenticated:
        return redirect("logIn")

    movie = get_object_or_404(Movie, movieID = movie_id)

    try:
        rating = Rating.objects.get(userID = request.user.id, movieID = movie_id)
    except Rating.DoesNotExist:
        rating = Rating()
        rating.userID = request.user.id
        rating.movieID = movie_id

    if request.method == "POST":
        ratingValue = request.POST["rating"]
        rating.rating = int(ratingValue)
        rating.save()
        # add message here
        return HttpResponseRedirect('/movieRecommendation/index')
    
    return render(request, 'movieRecommendation/movieDetail.html', {"movie": movie, "rating": rating})
    

    
def signUp(request):

    lastID = User.objects.last().id

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.id = lastID + 1
            username = form.cleaned_data.get('username')

            # create RecommendationHistory for new user
            if not alreadyHasRecHistory(user.id):
                recHistory = RecommendationHistory()
                recHistory.userID = user.id
                recHistory.save()
    
            login(request, user)
            return redirect("homepage")
        
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request, 'movieRecommendation/signUp.html', {"form": form})

    form = UserCreationForm
    return render(request, 'movieRecommendation/signUp.html', {"form": form})



def logOut(request):
    logout(request)
    return redirect("logIn")



def logIn(request):

    if request.method == "POST":

        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                 # create RecommendationHistory for user if it doesn't exist
                if not alreadyHasRecHistory(user.id):
                    recHistory = RecommendationHistory()
                    recHistory.userID = user.id
                    recHistory.save()

                login(request, user)
                return redirect("homepage")
                
            else:
                messages.error(request, "Invalid login attempt")

        else:
            messages.error(request, "Invalid login attempt")
        
    form = AuthenticationForm()
    return render(request, 'movieRecommendation/logIn.html', {"form": form})