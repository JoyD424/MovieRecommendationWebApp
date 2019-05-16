from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Movie(models.Model):
    movieID = models.IntegerField(default = 0)
    movieTitle = models.CharField(max_length = 200)
    movieGenres = models.CharField(max_length = 200)



class Rating(models.Model):
    userID = models.IntegerField(
        default = 0
    )

    movieID = models.IntegerField(
        default = 0
        )

    rating = models.IntegerField(
        default = 0,
        validators = [MaxValueValidator(5), MinValueValidator(0)]
        )



class RecommendationHistory(models.Model):
    userID = models.IntegerField(default=0)
    recommendations = models.CharField(max_length = 50000) # List Int stored as a string, separated by commas: "1,2,345,6"