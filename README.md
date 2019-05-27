# Movie Recommender
A web application that uses matrix factorization to recommend movies to users. Features include user login, logout, and signup capabilities.  
This project makes use of the following: Django web framework, SQLite database, MovieLens 1M Dataset, & TMDB API.   



## Preview
### User Homepage:
Displays the movies rated by and recommended for the user.  
This page can only be accessed if the user is verified and has rated movies.  
The user will be redirected to the index if no movies have been rated yet.  
![](images/homepageRatedMovies.png)
![](images/homepageRecs.png)

### Index:
Displays all movies stored in the database. The user can sort through the results by genre, title, etc.  
![](images/indexSearch.png)

### Movie Specifics:
Displays details for a specific movie, and allows the user to rate or modify their rating to the movie.  
![](images/movieDetail.png)



## System Requirements
Software:
```
Python 3+
Django 2.2
```
Python Libraries:
```
Numpy
Scipy
Pandas
```



## How To
After making sure all system requirements have been fulfilled:
1. Clone this repository. 
2. In Terminal or another command line interface, go to the location of the cloned repository.
3. Run `python manage.py runserver` on command line.
4. Go to `http://localhost:8000/movieRecommendation/` or `http://127.0.0.1:8000/movieRecommendation/` in a browser window.
