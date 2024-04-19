import os
import json
from threading import Thread
from django.shortcuts import render
from django.http import JsonResponse
from .utils import json_to_movies, first_10, json_to_data, take_movies
from .agents import Agent
from time import sleep, time
from .recommend import recommend

ratings = {}
movies = {}
genome = {}
time_mouse = {}
time_page = {}
searched = []
agent = 0
last_recommend = []

def json_to_ratings():
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
    global movies
    movies = json_to_movies()

    thread1 = Thread(target=json_to_ratings)
    thread2 = Thread(target=json_to_genome)
    thread1.start()
    thread2.start()

    init = first_10(movies)
    context = { 'init': init.items() }
    return render(request, 'index.html', context)

def search(request):
    global searched
    data = request.POST.get('data')
    result = {}

    for m in movies:
        if data in movies[m]['name'].lower():
            searched.append(int(m))
            result[m] = movies[m]

    context = { 'search': result.items() }
    return render(request, 'search.html', context)    

def create_agent(data):
    global agent, last_recommend
    
    while len(genome) == 0: sleep(1)

    agent = Agent(data, genome, movies)

    while len(last_recommend) == 0: sleep(1)

    agent.perceive(last_recommend, genome, movies)
          
def recomm(request):
    global agent, last_recommend
    data = request.POST.get('data')
    comments = request.POST.get('comments')
    data = json_to_data(data)
    comments = json_to_data(comments)

    #agent_maker = Thread(target=create_agent, args=(data,))
    #agent_maker.start()

    last_recommend = recommend(data, ratings)
    rec = take_movies(last_recommend, movies)
    context = { 'recommended': rec.items() }
    return render(request, 'recommended.html', context)  

def movie(request):
    data = json.loads(request.body)
    id = data.get('id')
    new_url = f"http://127.0.0.1:8000/movie/{id}/"
    return JsonResponse({'new_url': new_url})

def movie_id(request, id):
    mov = movies[int(id)]
    return render(request, 'movie.html', { 'data': mov })

def save_duration(request):
    global time_mouse
    data = json.loads(request.body)
    time = data.get('time')
    id = data.get('id')

    try:
        time_mouse[id] += time
    except:
        time_mouse[id] = time

    return JsonResponse({'status': 'ok'})

def ping(request, id):
    global time_page
    now = time()
    data = json.loads(request.body)
    id = data.get('id')

    try:
        length = len(time_page[id])
        if length % 2 == 0:
            val = time_page[id][length-1]
            if now - val > .3:
                time_page[id].append(now)
            else:
                time_page[id][length-1] = now
        else:
            time_page[id].append(now)
    except:
        time_page[id] = [now]

    return JsonResponse({'status': 'ok'})