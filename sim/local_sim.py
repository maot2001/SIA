from agents import Agent
from recommend import recommend
from views import json_to_genome, json_to_ratings, json_to_movies
from utils import take_movies

init = { 1: 1, 13: 1, 44: 0, 111: 1, 192: 1, 340: 0, 356: 1, 1006: 1, 1219: 0, 1258: 1, 1791: 0, 2459: 0 }

movies = json_to_movies()
genome = json_to_genome()
users = json_to_ratings()

agent = Agent(init, genome, movies)

for i in range(1, 5):
    last_rec, users_rec = recommend(init, users)
    temp = take_movies(last_rec, movies)
    for m in temp:
        print(temp[m]['name'])
    likes_id, dislikes_id = agent.perceive(last_rec, genome, movies, users_rec)

for e in agent.movies:
    print(e[0])
    print(e[1])
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