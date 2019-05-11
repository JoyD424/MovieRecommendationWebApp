from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Movie, Rating
from .recommendationEngine import runRecEngine


def index(request):
    allMovies = Movie.objects.all()
    return render(request, 'movieRecommendation/index.html', {'allMovies': allMovies})


def movieDetail(request, movie_id):
    movie = get_object_or_404(Movie, id = movie_id)
    return render(request, 'movieRecommendation/movieDetail.html', {'movie': movie})


def recommendation(request):

    if not request.user.is_authenticated:
        return redirect("logIn")

    user_id = request.user.id
    alreadyRatedList, predictionsList = runRecEngine(user_id)
    print(len(predictionsList)) # TEST
    alreadyRatedMovies, predictionsMovies = [], []
    movieRatingDict = {}

    for tuple in alreadyRatedList:
        movie = get_object_or_404(Movie, id = tuple[0])
        alreadyRatedMovies.append(movie)
        if movie.movieID not in movieRatingDict.keys():
            movieRatingDict[movie.movieID] = tuple[1]

    for tuple in predictionsList:
        movie = get_object_or_404(Movie, id = tuple[0])
        predictionsMovies.append(movie)
        if movie.movieID not in movieRatingDict.keys():
            movieRatingDict[movie.movieID] = tuple[1]

    return render(request, 'movieRecommendation/recommendation.html', {'alreadyRatedMovies': alreadyRatedMovies, 'predictionsMovies': predictionsMovies, 'movieRatingDict': movieRatingDict})

    
def signUp(request):

    lastID = User.objects.last().id

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.id = lastID + 1
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("index")
        
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
                login(request, user)
                return redirect("index")
                
            else:
                messages.error(request, "Invalid login attempt")

        else:
            messages.error(request, "Invalid login attempt")
        
    form = AuthenticationForm()
    return render(request, 'movieRecommendation/logIn.html', {"form": form})


    
