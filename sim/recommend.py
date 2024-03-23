from random import choice
    
def jaccard(movies: dict, ratings: dict):
    """Determine nearest users using Jaccard distance.

    Args:
        movies (dict): The user website ratings.
        ratings (dict): The user ratings database.

    Returns:
        list((int, float, int)): Returns the users organized descendingly by the Jaccard distance and then by the Union value,
                                 in the first position is the user id, in the second the Jaccard distance and in the third the
                                 Union.
    """
    user = []
    mov_index = list(movies.keys())
    for r in ratings:
        intersection, union = 0, 0
        index1, index2 = 0, 0
        rat_index = list(ratings[r].keys())
        rat_index.remove('name')

        # Iterating through the id movies of the website user and user r in the database
        while index1 < len(mov_index) and index2 < len(rat_index):
            if mov_index[index1] < rat_index[index2]: index1 += 1
            elif mov_index[index1] > rat_index[index2]: index2 += 1
            
            # When the ids match (that is, both users have given an opinion about the same movie)
            else:
            
                # If the value matches, they have the same opinion, which is added to the intersection
                if movies[mov_index[index1]] == ratings[r][rat_index[index2]]: intersection +=1
                index1 += 1
                index2 += 1

            # In each iteration, a movie is advanced about which at least one of the two users has given their opinion, 
            # so it belongs to the union.
            union += 1
        union += (len(mov_index) - index1 + len(rat_index) - index2)

        if intersection != 0 and union != 0: user.append((r, intersection/union, union))
    
    return sorted(user, key=lambda x: (x[1], x[2]), reverse=True)

def recommend(movies: dict, ratings: dict):
    """Using the Jaccard distance, it generates recommendations of at most 10 movies.

    Args:
        movies (dict): The user website ratings.
        ratings (dict): The user ratings database.

    Returns:
        list(int): Recommended movies id.
        list(str): Each position corresponds to the user who made the recommendation in the position in the previous list.
    """
    jac = jaccard(movies, ratings)
    sug = []
    users = []
    mov_index = list(movies.keys())
    
    for j in jac:
        rat_index = list(ratings[j[0]].keys())
        rat_index.remove('name')
        rat_good = []

        # Adding positive user recommendations
        for r in rat_index:
            if ratings[j[0]][r]: rat_good.append(r)
    
        # Removing movies that the user has already seen from the website
        for m in mov_index:
            if m in rat_good: rat_good.remove(m)

        # Removing movies that have already been recommended
        for s in sug:
            if s in rat_good: rat_good.remove(s)
    
        # Selection of recommendations
        n = min(10 - len(sug), 3, len(rat_good))
        while n > 0:
            temp = choice(rat_good)
            rat_good.remove(temp)
            sug.append(temp)
            users.append(ratings[j[0]]['name'])
            n -= 1

        if len(sug) >= 10: break

    return sug, users
        