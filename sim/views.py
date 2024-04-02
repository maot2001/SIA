import os
import json
from threading import Thread
from django.shortcuts import render
from django.http import JsonResponse
from .utils import json_to_movies, first_10, json_to_data, take_movies
from .agents import Agent
from time import sleep
from .recommend import recommend
#from utils import json_to_movies, first_10, json_to_data, take_movies

ratings = {}
movies = {}
genome = {}
agent = 0
last_recommend = []
users = []

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
    data = request.POST.get('data')
    result = {}

    for m in movies:
        if data in movies[m]['name'].lower():
            result[m] = movies[m]

    context = { 'search': result.items() }
    return render(request, 'index.html', context)    

def create_agent(data):
    global agent, last_recommend, users
    
    while len(genome) == 0: sleep(1)

    agent = Agent(data, genome, movies)

    while len(last_recommend) == 0: sleep(1)

    for i in range(4):
        mov = take_movies(agent.perceive(last_recommend, genome, movies, users), movies)
        for m in mov:
            print(mov[m]['name'])
        last_recommend, users = recommend(agent.val, ratings)

    for e in agent.likes:
        print(e['name'])
        print("----------------------------------------------------------------------------")
    print()

    for e in agent.dislikes:
        print(e['name'])
        print("----------------------------------------------------------------------------")
    print()

    for e in agent.believes.likes:
        print(e[0])
    print()

    for e in agent.believes.dislikes:
        print(e[0])
    print()

    for e in agent.believes.text:
        print(e)
    print()
          
def recomm(request):
    global agent, last_recommend, users
    data = request.POST.get('data')
    data = json_to_data(data)

    agent_maker = Thread(target=create_agent, args=(data,))
    agent_maker.start()

    last_recommend, users = recommend(data, ratings)
    rec = take_movies(last_recommend, movies)
    context = { 'recommended': rec.items() }
    return render(request, 'index.html', context)  

def guardar_duracion(request):
    print('init')
    if request.method == 'POST':
        print('post')
        data = json.loads(request.body)
        duration = data.get('duration')
        print(duration)
        
        # Aquí puedes guardar la duración en la base de datos o realizar otras acciones
        # Ejemplo de guardado en la base de datos:
        # TuModeloDuracion.objects.create(duration=duration)
        
        return JsonResponse({'message': 'Duración guardada correctamente'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
"""
def process_data(request):
    print('in_process_data')
    data = request.POST.get('search')  # Obtener la información del frontend
    print(data)
    data = 'data'  # Obtener la información del frontend

    # Iniciar un hilo para procesar la información en segundo plano
    thread = Thread(target=process_data_in_background, args=(data,))
    thread.start()

    print('pass_thread')
    return JsonResponse({'message': 'Data processing started'})

def process_data_in_background(data):
    print('in_thread')
    channel_layer = lay.get_channel_layer()
    async_to_sync(channel_layer.group_send)('custom_channel', {'type': 'send_message', 'message': data})
"""