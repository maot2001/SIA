from random import choice
import os
import json
from math import sqrt

def json_to_movies():
    """Load movie database.

    Returns:
        dict: id_movie (int): { type: str, 
                                name: str,
                                url (url to the movie page on the IMDB website): str,
                                poster (url to the movie poster image): str,
                                description: str,
                                review (dict): { author: str,
                                                 dateCreated: str,
                                                 inLanguage: str,
                                                 heading: str,
                                                 reviewBody: str,
                                                 reviewRating (dict): { worstRating: int
                                                                        bestRating: int
                                                                        ratingValue: int}
                                },
                                rating (dict): { ratingCount: int,
                                                 bestRating: int,
                                                 worstRating: int,
                                                 ratingValue: float},
                                contentRating: str,
                                genre: list(str),
                                datePublished: str,
                                keywords: str,
                                duration: str,
                                actor: list(dict: { name: str,
                                                    url: (url to the actor page on the IMDB website)}),
                                director: list(dict: { name: str,
                                                    url: (url to the director page on the IMDB website)),
                                creator: list(dict: { name: str,
                                                    url: (url to the creator page on the IMDB website)})
        }
    """
    route = os.getcwd()
    route = os.path.join(route, 'data')
    route = os.path.join(route, 'movie.json')

    with open(route, 'r', encoding='utf-8') as json_file:
        content = json.load(json_file)

    movies = {}

    for mov in content:
        movies[int(mov)] = content[mov]
   
    return movies

def json_to_data(data: str):
    """Load the user user ratings of movies found on the website.

    Args:
        data (str): User rating of movies.

    Returns:
        dict: { id_movie (int): 1 (if like) or 0 (if dislike) }
    """
    content = json.loads(data)

    movies = {}

    for mov in content:
        movies[int(mov)] = content[mov]
   
    return movies

def first(movies: dict):
    """Random movie selector to start the page.

    Args:
        movies (dict): The movie database.

    Returns:
        dict: Movie Database Items.
    """
    n = 30
    init = {}
    to_choice = list(movies.keys())
    
    while n > 0:
        temp = choice(to_choice)
        init[temp] = movies[temp]
        n = 30 - len(init)
    
    return init

# For cosine similarity
def sum_mult_vector(believe, recommended):
  return sum(believe[i] * recommended[i] for i in range(len(believe)))

# For cosine similarity
def sum_dist_vector(vector):
  return sqrt(sum(vector[i]**2 for i in range(len(vector))))

def cosine(believe, recommended):
    """Cosine similarity.
    """
    return sum_mult_vector(believe, recommended)/ (sum_dist_vector(believe) * sum_dist_vector(recommended))

def take_movies(recommended, movies):
    """Auxiliary method to obtain movies from the database having their id.
    """
    mov = {}
    for i in recommended:
        mov[i] = movies[i]
    return mov

def cort(response, sep: str):
    """Parser of separators between elements in the initial response of LM-studio.

    Args:
        response (str): Initial response.
        sep (str): Separators.

    Returns:
        list(str): All elements found between pairs of separators.
    """
    if not sep in response: return None
    init = response.find(sep)
    end = response[init + len(sep):].find(sep[::-1])
    result = []
    aux = 0

    while init >= 0:
        result.append(response[aux + init + len(sep) :aux + init + len(sep) + end])
        aux += init + 2 * len(sep) + end
        init = response[aux:].find(sep)
        end = response[aux + init + len(sep):].find(sep[::-1])

    return result