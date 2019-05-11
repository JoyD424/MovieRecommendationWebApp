from django.urls import path
from . import views

urlpatterns = [
    # ex: /movieRecommendation/
    path('', views.index, name='index'),

    # ex: /movieRecommendation/1/
    path('<int:movie_id>/', views.movieDetail, name='movieDetail'),

    # ex: /movieRecommendation/1/recommendation/
    path('recommendation/', views.recommendation, name='recommendation'),

    # ex: /movieRecommendation/signUp/
    path('signUp/', views.signUp, name='signUp'),

    # ex: /movieRecommendation/logout/
    path('logOut/', views.logOut, name='logOut'),

    path('logIn/', views.logIn, name='logIn'),
]   
