from django.urls import path
from . import views

urlpatterns = [
    # ex: /movieRecommendation/
    path('', views.homepage, name='homepage'),

    # ex: /movieRecommendation/index/
    path('index/', views.index, name='index'), 

    # ex: /movieRecommendation/1/
    path('<int:movie_id>/', views.movieDetail, name='movieDetail'),

    # ex: /movieRecommendation/signUp/
    path('signUp/', views.signUp, name='signUp'),

    # ex: /movieRecommendation/logout/
    path('logOut/', views.logOut, name='logOut'),

    # ex: /movieRecommendation/logout/
    path('logIn/', views.logIn, name='logIn'),
]   
