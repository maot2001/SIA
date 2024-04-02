from random import choice
    
def jaccard(movies: dict, ratings: dict):
    user = []
    mov_index = list(movies.keys())
    for r in ratings:
        intersection, union = 0, 0
        index1, index2 = 0, 0
        rat_index = list(ratings[r].keys())
        rat_index.remove('name')

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

def recommend(movies: dict, ratings: dict):
    jac = jaccard(movies, ratings)
    sug = []
    users = []
    mov_index = list(movies.keys())
    
    for j in jac:
        rat_index = list(ratings[j[0]].keys())
        rat_index.remove('name')
        rat_good = []
        for r in rat_index:
            if ratings[j[0]][r]: rat_good.append(r)
    
        for m in mov_index:
            if m in rat_good: rat_good.remove(m)

        for s in sug:
            if s in rat_good: rat_good.remove(s)
    
        n = min(10 - len(sug), 3, len(rat_good))
        while n > 0:
            temp = choice(rat_good)
            rat_good.remove(temp)
            sug.append(temp)
            users.append(ratings[j[0]]['name'])
            n -= 1

        if len(sug) >= 10: break

    return sug, users
        