from random import randint, sample
from scipy.sparse import csr_matrix
import numpy as np
from implicit.als import AlternatingLeastSquares
    
def jaccard_distance(movies: dict, ratings: dict):
    user = []
    mov_index = list(movies.keys())
    for r in ratings:
        intersection, union = 0, 0
        index1, index2 = 0, 0
        rat_index = list(ratings[r].keys())

        while index1 < len(mov_index) and index2 < len(rat_index):
            if mov_index[index1] < rat_index[index2]: index1 += 1
            elif mov_index[index1] > rat_index[index2]: index2 += 1
            else:
                if movies[mov_index[index1]] == ratings[r][rat_index[index2]]: intersection +=1
                index1 += 1
                index2 += 1
            union += 1
        union += (len(mov_index) - index1 + len(rat_index) - index2)

        if intersection != 0 and union != 0: user.append((r, intersection/union, union))
    
    return sorted(user, key=lambda x: (x[1], x[2]), reverse=True)

def jaccard_recommend(movies: dict, ratings: dict):
    jac = jaccard_distance(movies, ratings)
    sug = []
    mov_index = list(movies.keys())
    threshold = .1
    
    for j in jac:
        if j[1] <= threshold: 
            if len(sug) > 50: break
            elif threshold < .05:
                if len(sug) > 20: break
                elif threshold == 0:
                    raise Exception("The information provided is insufficient")
                else:
                    threshold -= .01
            else:
                threshold -= .01

        rat_index = list(ratings[j[0]].keys())
        rat_good = []
        for r in rat_index:
            if ratings[j[0]][r]: rat_good.append(r)
    
        for m in mov_index:
            if m in rat_good: rat_good.remove(m)

        for s in sug:
            if s in rat_good: rat_good.remove(s)
    
        sug.extend(rat_good)

    return sug
        
def recommend(movies: dict, ratings: dict):
    ids_movies = jaccard_recommend(movies, ratings)

    ids_movies = sorted(ids_movies)
    keys = ratings.keys()
    key = max(keys)
    matrix = np.zeros((key, len(ids_movies)))

    for i in ratings:
        for j in ratings[i]:
            if i > len(ratings): break
            if j in ids_movies:
                index = ids_movies.index(j)
                if ratings[i][j]:
                    matrix[i - 1][index] = 1
                else:
                    matrix[i - 1][index] = -1

    num_movies = 10
    size_poblation = 1000
    num_generations = 20
    size_select = 5
    matrix_sparse = csr_matrix(matrix)
    als_model = AlternatingLeastSquares(factors=50, regularization=0.01)
    als_model.fit(matrix_sparse)

    def evaluate(ids_movies):
        quality = 0
        
        for i, id_movie in enumerate(ids_movies):
            represent = als_model.item_factors[id_movie]
            sim = np.dot(represent, als_model.user_factors.T)
            quality_mov = np.sum(sim * matrix[:, i])
            quality += quality_mov
        
        return quality

    def init_pob():
        poblation = []
        for _ in range(size_poblation):
            recommend = [randint(0, len(ids_movies) - 1) for i in range(num_movies)]
            poblation.append(recommend)
        return poblation

    def select(poblation):
        selected = sample(poblation, size_select)
        best_recommend = max(selected, key=evaluate)
        return best_recommend

    def crossing(father1, father2):
        crossing_point = randint(1, num_movies - 1)
        son = [father1[k] if i < crossing_point else father2[k] for i, k in enumerate(range(len(father1)))]
        return son
    
    def mutate(son):
        for i in range(len(son)):
            if np.random.random() < .01:
                son[i] = randint(0, len(ids_movies) - 1)
        return son

    poblation = init_pob()

    for _ in range(num_generations):
        new_poblation = []
        for _ in range(size_poblation):
            father1 = select(poblation)
            father2 = select(poblation)
            son = crossing(father1, father2)
            son = mutate(son)
            new_poblation.append(son)

        poblation = new_poblation

    best = set(max(poblation, key=evaluate))
    return [ids_movies[i] for i in best]