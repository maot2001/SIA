from random import choice
import os
import json
from math import sqrt

def json_to_movies():
    route = os.getcwd()
    route = os.path.join(route, 'data')
    route = os.path.join(route, 'movie.json')

    with open(route, 'r', encoding='utf-8') as json_file:
        content = json.load(json_file)

    movies = {}

    for mov in content:
        movies[int(mov)] = content[mov]
   
    return movies

def json_to_data(data):
    content = json.loads(data)

    movies = {}

    for mov in content:
        movies[int(mov)] = content[mov]
   
    return movies

def first_10(movies):
    n = 30
    init = {}
    to_choice = list(movies.keys())
    
    while n > 0:
        temp = choice(to_choice)
        init[temp] = movies[temp]
        n = 30 - len(init)
    
    return init

def sum_mult_vector(believe, recommended):
  return sum(believe[i] * recommended[i] for i in range(len(believe)))

def sum_dist_vector(vector):
  return sqrt(sum(vector[i]**2 for i in range(len(vector))))

def take_movies(recommended, movies):
    mov = {}
    for i in recommended:
        mov[i] = movies[i]
    return mov

def cort(response, sep):
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