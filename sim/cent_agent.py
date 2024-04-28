from numpy.random import random
from .com_agent import Com_Agent
from .diffuse import DifusseAgent
from .vect_agent import Vect_Agent

class Cent_Agent:
    def __init__(self, data: dict, comments: dict, movies: dict, genome: dict):
        self.com_agent = Com_Agent(comments, movies)
        self.diff_agent = DifusseAgent(data, movies)
        self.vect_agent = Vect_Agent(data, genome)

    def perceive(self, recommend: list, movies: dict, genome: dict):
        com_eval = self.com_agent.perceive(recommend, movies)
        self.diff_agent.perceive(recommend, movies)
        diff_eval = self.diff_agent.recommended_like
        vect_eval = self.vect_agent.perceive(recommend, genome)

        result = {}
        for i in range(len(recommend)):
            diff = 1 if recommend[i] in diff_eval else 0
            vect = vect_eval[i]
            if com_eval:
                com = com_eval[i]
                val = .5 * diff + .3 * vect + .2 * com
            else:
                val = .6 * diff + .4 * vect

            if val > .7:
                result[recommend[i]] = True
            elif val < .3:
                result[recommend[i]] = False
            else:
                aleat = random()
                decition = (aleat < val)
                result[recommend[i]] = decition

        print(result)