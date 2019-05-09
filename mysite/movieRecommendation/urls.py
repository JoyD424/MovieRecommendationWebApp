from django.urls import path
from . import views

urlpatterns = [
    # ex: /movieRecommendation/
    path('', views.index, name='index'),

    # ex: /movieRecommendation/1/
    path('<int:movie_id>/', views.movieDetail, name='movieDetail'),

    # ex: /movieRecommendation/1/recommendation/
    path('<int:user_id>/recommendation', views.recommendation, name='recommendation')
]