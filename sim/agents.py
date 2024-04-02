from numpy.random import random
from time import time
from .utils import sum_dist_vector, sum_mult_vector, cort
from .ai_compare import *
#from utils import sum_dist_vector, sum_mult_vector, cort
#from ai_compare import *

class Belief:
    def __init__(self, liked, genome, movies):
        self.likes = []
        self.dislikes = []
        self.init_belief_genre(liked, genome)

        self.text = []
        self.update_belief_text(liked, movies)

        self.clasify={}
        self.duration={}

    def init_belief_genre(self, liked, genome):
        for movie in liked:
            if liked[movie] == 1: add_genoma(self.likes, genome[movie])
            else: add_genoma(self.dislikes, genome[movie])

    def update_belief_text(self, liked, movies):
        mov_likes = []
        mov_dislikes = []
        for movie in liked:
            if liked[movie] == 1: mov_likes.append(movie)
            else: mov_dislikes.append(movie)

        response = descriptions(mov_likes, movies, 'like')
        self.parse_response(response)
        
        response = descriptions(mov_dislikes, movies, 'dislike')
        self.parse_response(response)

        response = keywords(mov_likes, movies, 'like')
        self.parse_response(response)
        
        response = keywords(mov_dislikes, movies, 'dislike')
        self.parse_response(response)

        response = actors(mov_likes, movies, 'like')
        self.parse_response(response)

        response = actors(mov_dislikes, movies, 'dislike')
        self.parse_response(response)

        response = directors(mov_likes, movies, 'like')
        self.parse_response(response)

        response = directors(mov_dislikes, movies, 'dislike')
        self.parse_response(response)

        response = creators(mov_likes, movies, 'like')
        self.parse_response(response)

        response = creators(mov_dislikes, movies, 'dislike')
        self.parse_response(response)

        print("The belief's:")
        print(self.text)

    def parse_response(self, response):
        if response: 
            print(response)
            tmp = []
            
            for r in response:
                any_parse = False
                init = r.find("and I like")
                if init != -1:
                    any_parse = True
                    tmp.append(r[: init - 1])
                    tmp.append(r[init + 4:])
                init = r.find("and I dislike")
                if init != -1:
                    any_parse = True
                    tmp.append(r[: init - 1])
                    tmp.append(r[init + 4:])
                if not any_parse:
                    aux = r.split(',')
                    for e in aux:
                        e2 = e.strip()
                        aux2 = e2.split('.')
                        for f in aux2:
                            if f != '':
                                tmp.append(f)

            print(tmp)
            for b in tmp:
                if not b in self.text:
                    init = 'dislike' if 'dislike' in b else 'like'
                    end = 'like' if init == 'dislike' else 'dislike'
                    aux = b.replace(init, end)
                    if aux in self.text: 
                        if 'dislike' in aux:
                            self.text.remove(aux)
                            self.text.append(b)
                    else: self.text.append(b)


    def update_belief_clasify(self,key,value):
        self.clasify[key]=value
    def update_belief_duration(self,key,value):
        self.duration[key]=value
    def get_belief(self,key):
        return self.beliefs[key]

def add_genoma(to_add, add_value, like=True):
    if len(to_add) == 0:
        to_add.append([1, add_value])
    else:
        new = True
        for val in to_add:
            cos = sum_mult_vector(val[1], add_value)/ (sum_dist_vector(val[1]) * sum_dist_vector(add_value))
            if cos > .7:
                if like:
                    val[1] = [((val[0] * val[1][e]) + add_value[e]) / (val[0] + 1) for e in range(len(val[1]))]
                else:
                    val[1] = [((val[0] * val[1][e]) - add_value[e]) / (val[0] + 1) for e in range(len(val[1]))]
                    val[1] = [0 if val[1][e] < 0 else val[1][e] for e in range(len(val[1]))]
                val[0] += 1
                new = False
        if new and like: to_add.append([1, add_value])

def create_environment(movies, data):
    genres=[]
    for item in movies:
        genres.append({'id':item,'values':data[item]})
    return genres

class Agent:
    def __init__(self, liked: dict, genome: dict, movies: dict):
        self.believes = Belief(liked, genome, movies)
        self.val = liked
        self.likes = [[movies[m] for m in liked if liked[m] == 1]]
        self.dislikes = [[movies[m] for m in liked if liked[m] == 0]]
        self.recommended = {}
    
    def perceive(self, recom, genome, movies, users):
        genres = create_environment(recom, genome)
        likes = []
        dislikes = []
        
        likes_id = []
        dislikes_id = []

        for i in range(len(genres)):
            closer = []
            max_cos = 0
            for b in self.believes.likes:
                cos = sum_mult_vector(genres[i]['values'], b[1])/ (sum_dist_vector(genres[i]['values']) * sum_dist_vector(b[1]))
                if cos > .7: closer.append(b)
                max_cos = max(max_cos, cos)

            a, b = len(likes), len(dislikes)
            
            self.action(max_cos, genres[i]['values'], closer, users[i], likes, dislikes, movies[genres[i]['id']])
            
            if a < len(likes): 
                likes_id.append(genres[i]['id'])
                self.val[genres[i]['id']] = 1
            if b < len(dislikes): 
                dislikes_id.append(genres[i]['id'])
                self.val[genres[i]['id']] = 0

        print(self.believes.text)
        self.likes.append(likes)
        self.dislikes.append(dislikes)
        self.believes.update_belief_text(self.val, movies)
        return self.val.keys()

    def add_desires(self):
        pass
    
    def action(self, cos, vector, closer, user, likes, dislikes, movie):
        if random() < cos:
            if random() < cos:
                likes.append(movie)
                add_genoma(self.believes.likes, vector, True)
                try: self.recommended[user] += cos
                except: self.recommended[user] = cos
                if self.recommended[user] > 2:
                    belief = f'I like {user}\'s recommendations'
                    if not belief in self.believes.text: self.believes.text.append(belief)
                if self.recommended[user] - cos < -2:
                    self.believes.text.remove(f'I dislike {user}\'s recommendations')
            else:
                dislikes.append(movie)
                if len(closer) > 0: add_genoma(self.believes.likes, vector, False)
                else: add_genoma(self.believes.dislikes, vector, True)
                try: self.recommended[user] -= cos
                except: self.recommended[user] = -cos
                if self.recommended[user] < -2:
                    belief = f'I dislike {user}\'s recommendations'
                    if not belief in self.believes.text: self.believes.text.append(belief)
                if self.recommended[user] + cos > 2:
                    self.believes.text.remove(f'I like {user}\'s recommendations')
