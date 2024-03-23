from numpy.random import random
from time import time
from .utils import cosine
from .ai_compare import *

class Belief:
    def __init__(self, liked: dict, genome: dict, movies: dict):
        """The Belief object is used to store the different types of beliefs of an Agent.

        Args:
            liked (dict): The user website ratings.
            genome (dict): The subgender valoration database.
            movies (dict): The movie database.
        """
        self.likes = []
        self.dislikes = []
        self.init_belief_genre(liked, genome)

        self.text = []
        self.update_belief_text(liked, movies)

        self.clasify={}
        self.duration={}

    def init_belief_genre(self, liked: dict, genome: dict):
        """Algebraic belief generator using cosine similarity.

        Args:
            liked (dict): The user website ratings.
            genome (dict): The subgender valoration database.
        """
        for movie in liked:
            if liked[movie] == 1: add_genoma(self.likes, genome[movie])
            else: add_genoma(self.dislikes, genome[movie])

    def update_belief_text(self, liked: dict, movies: dict):
        """Text belief generator using LM-Studio. In this, different parameters of the movies are used to generate text: 
            description, keywords, actors, directors and creators

        Args:
            liked (dict): The user website ratings.
            movies (dict): The movie database.
        """
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

    def parse_response(self, response):
        """Second parser to generate beliefs
        """
        if response: 
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
    """Function to add elements to the Agent's algebraic beliefs.

    Args:
        to_add (list(list(float))): The list of algebraic beliefs about movies you like or dislike.
        add_value (list(float))): The assessment of the weight of each subgenre of a movie.
        like (bool, optional): In the case of a recommended movie that the user did not like. Defaults to True.
    """
    if len(to_add) == 0:
        to_add.append([1, add_value])
    else:
        new = True
        for val in to_add:
            cos = cosine(val[1], add_value)
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
    """Auxiliary method to obtain genome of movies from the database having their id.
    """
    genres=[]
    for item in movies:
        genres.append({'id':item,'values':data[item]})
    return genres

class Agent:
    def __init__(self, liked: dict, genome: dict, movies: dict):
        """The Agent is the one who receives the user's information and reacts to the recommendations.

        Args:
            liked (dict): The user website ratings.
            genome (dict): The subgender valoration database.
            movies (dict): The movie database.
        """
        self.believes = Belief(liked, genome, movies)
        self.val = liked
        self.likes = [[movies[m] for m in liked if liked[m] == 1]]
        self.dislikes = [[movies[m] for m in liked if liked[m] == 0]]
        self.recommended = {}
    
    def perceive(self, recom: list, users: list, genome: dict, movies: dict):
        """Simulation of user reaction to recommendations

        Args:
            recom (list): Recommended movies id.
            users (list): Each position corresponds to the user who made the recommendation in the position in the previous list.
            genome (dict): The subgender valoration database.
            movies (dict): The movie database.
        Returns:
            _type_: _description_
        """
        genres = create_environment(recom, genome)
        likes = []
        dislikes = []
        
        likes_id = []
        dislikes_id = []

        for i in range(len(genres)):
            closer = []
            max_cos = 0

            # Save the maximum similarity between the user's tastes
            for b in self.believes.likes:
                cos = cosine(genres[i]['values'], b[1])
                if cos > .7: closer.append(b)
                max_cos = max(max_cos, cos)

            a, b = len(likes), len(dislikes)
            
            # Simulate the reaction to a movie recommendation.
            self.action(max_cos, genres[i]['values'], closer, users[i], likes, dislikes, movies[genres[i]['id']])
            
            if a < len(likes): 
                likes_id.append(genres[i]['id'])
                self.val[genres[i]['id']] = 1
            if b < len(dislikes): 
                dislikes_id.append(genres[i]['id'])
                self.val[genres[i]['id']] = 0

        self.likes.append(likes)
        self.dislikes.append(dislikes)
        self.believes.update_belief_text(self.val, movies)
        return self.val.keys()

    def add_desires(self):
        pass
    
    def action(self, cos: float, vector: list, closer: list, user: str, likes: list, dislikes: list, movie: dict):
        """Simulates and saves the information within the agent, using uniform variables and the cosine similarity value.

        Args:
            cos (float): Maximum similarity.
            vector (list): Value of each subgenre in the movie.
            closer (list): List of algebraic beliefs close to the film.
            user (str): Name of the user who made the recommendation.
            likes (list): List of movies you like among those recommended.
            dislikes (list): List of movies you dislike among those recommended.
            movie (dict): Movie from the movie database.
        """

        # The first time is done to simulate whether the user decides to watch the movie or not.
        if random() < cos:

            # If so, it is tested to find out if the user liked the movie or not.
            if random() < cos:
                likes.append(movie)
                add_genoma(self.believes.likes, vector, True)

                # The value of the recommendations is added to the user who made it, if a certain threshold is passed it is 
                # added to the text beliefs
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

                # The value of the recommendations is added to the user who made it, if a certain threshold is passed it is 
                # added to the text beliefs
                try: self.recommended[user] -= cos
                except: self.recommended[user] = -cos
                if self.recommended[user] < -2:
                    belief = f'I dislike {user}\'s recommendations'
                    if not belief in self.believes.text: self.believes.text.append(belief)
                if self.recommended[user] + cos > 2:
                    self.believes.text.remove(f'I like {user}\'s recommendations')
