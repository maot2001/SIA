import os
import json
from threading import Thread
from django.shortcuts import render
from .utils import json_to_movies, first, json_to_data, take_movies
from .agents import Agent
from time import sleep
from .recommend import recommend

ratings = {}
movies = {}
genome = {}
agent = 0
last_recommend = []
users = []

def json_to_ratings():
    """Load the user ratings json.

    Returns:
        dict: id_user (int): { name: str, 
                               ratings: dict( id_movie (int): 1 (if like) or 0 (if dislike) ) }
    """
    global ratings
    route = os.getcwd()
    route = os.path.join(route, 'data')
    route = os.path.join(route, 'users.json')

    with open(route, 'r', encoding='utf-8') as json_file:
        content = json.load(json_file)

    for rat in content:
        key = int(rat)
        ratings[key] = {}
        for val in content[rat]['ratings']:
            ratings[key][int(val)] = content[rat]['ratings'][val]
        ratings[key]['name'] = content[rat]['name']

    return ratings
   
def json_to_genome():
    """Subgenre relationship load with each movie.

    Returns:
        dict: id_movie (int): list(float) (the tag of every position is in tags.json file in the same position)
    """
    global genome
    route = os.getcwd()
    route = os.path.join(route, 'data')
    route = os.path.join(route, 'genome.json')

    with open(route, 'r', encoding='utf-8') as json_file:
        content = json.load(json_file)

    for gen in content:
        genome[int(gen)] = content[gen]
    
    return genome
   
def start(request):
    """It is responsible for loading the databases and returning a home page with different randomly selected movies.

    Args:
        request (): Initial request when connecting to the server.

    Returns:
        HttpResponse: Home Page.
    """
    print(type(request))
    # Loading database
    global movies
    movies = json_to_movies()
    thread1 = Thread(target=json_to_ratings)
    thread2 = Thread(target=json_to_genome)
    thread1.start()
    thread2.start()

    # Movie selection
    init = first(movies)
    context = { 'init': init.items() }
    return render(request, 'index.html', context)

def search(request):
    """Movie search engine linked to the website search bar.

    Args:
        request (): In the data element you will find the search performed by the user.

    Returns:
        HttpResponse: List of found movies, particular interface of a single movie or Not Found.
    """
    data = request.POST.get('data')
    result = {}

    # Search
    for m in movies:
        if data in movies[m]['name'].lower():
            result[m] = movies[m]

    context = { 'search': result.items() }
    return render(request, 'index.html', context)    

def create_agent(data: dict):
    """Creation and interaction of the user reaction simulator agent.

    Args:
        data (dict: id_movie (int): 1 (if like) or 0 (if dislike)): User rating of movies obtained on the website.
    """
    global agent, last_recommend, users
    
    # Wait for subgenre database
    while len(genome) == 0: sleep(1)

    agent = Agent(data, genome, movies)

    # Wait for the system recommendation
    while len(last_recommend) == 0: sleep(1)

    # Simulation
    for i in range(4):
        mov = take_movies(agent.perceive(last_recommend, genome, movies, users), movies)
        last_recommend, users = recommend(agent.val, ratings)
 
def recomm(request):
    """Recommendation system that uses the Jaccard distance.

    Args:
        request (): In the data element there are user ratings of movies found on the website.

    Returns:
        HttpResponse: List with 10 recommendations or less selected based on opinions of the closest users.
    """
    global agent, last_recommend, users
    data = request.POST.get('data')
    data = json_to_data(data)

    # Agent running in the background
    agent_maker = Thread(target=create_agent, args=(data,))
    agent_maker.start()

    # Recommendation system
    last_recommend, users = recommend(data, ratings)
    rec = take_movies(last_recommend, movies)
    context = { 'recommended': rec.items() }
    return render(request, 'index.html', context)  
