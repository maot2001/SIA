from .utils import sum_dist_vector, sum_mult_vector

class Belief:
    def __init__(self, liked, genome):
        self.likes = []
        self.dislikes = []
        for movie in liked:
            if not movie in genome: continue
            if liked[movie] == 1: add_genoma(self.likes, genome[movie])
            else: add_genoma(self.dislikes, genome[movie])

def add_genoma(to_add, add_value):
    if len(to_add) == 0:
        to_add.append([1, add_value])
    else:
        new = True
        for val in to_add:
            cos = sum_mult_vector(val[1], add_value)/ (sum_dist_vector(val[1]) * sum_dist_vector(add_value))
            if cos > .7:
                val[1] = [((val[0] * val[1][e]) + add_value[e]) / (val[0] + 1) for e in range(len(val[1]))]
                val[0] += 1
                new = False
        if new: to_add.append([1, add_value])

class Vect_Agent:
    def __init__(self, liked: dict, genome: dict):
        self.belief = Belief(liked, genome)
    
    def perceive(self, recommend: list, genome: dict):
        result = []

        for i in recommend:
            if not i in genome:
                result.append(0)
                continue
            
            pos_cos, neg_cos = 0, 0

            for b in self.belief.likes:
                cos = sum_mult_vector(genome[i], b[1])/ (sum_dist_vector(genome[i]) * sum_dist_vector(b[1]))
                pos_cos = max(pos_cos, cos)

            for b in self.belief.dislikes:
                cos = sum_mult_vector(genome[i], b[1])/ (sum_dist_vector(genome[i]) * sum_dist_vector(b[1]))
                neg_cos = max(neg_cos, cos)

            if pos_cos >= neg_cos:
                result.append(pos_cos)
            else:
                result.append(-neg_cos)

        return result