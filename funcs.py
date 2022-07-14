def get_movie_lists(movies):
    '''Get separate lists of movies for easier display'''

    movies1 = list(movies['results'])[:4]
    movies2 = list(movies['results'])[4:8]
    movies3 = list(movies['results'])[8:12]
    movies4 = list(movies['results'])[12:16]
    

    return [movies1, movies2, movies3, movies4]
