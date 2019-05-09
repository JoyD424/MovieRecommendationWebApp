from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Movie, Rating
from .recommendationEngine import runRecEngine


def index(request):
    allMovies = Movie.objects.all()
    return render(request, 'movieRecommendation/index.html', {'allMovies': allMovies})


def movieDetail(request, movie_id):
    movie = get_object_or_404(Movie, id = movie_id)
    return render(request, 'movieRecommendation/movieDetail.html', {'movie': movie})


def recommendation(request, user_id):
    alreadyRatedList, predictionsList = runRecEngine(user_id)
    