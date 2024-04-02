from openai import OpenAI
from .utils import cort
#from utils import cort
from time import time

seps = ['"', '```\n']

init = 'I want the relationship between the following elements, in the questions are the elements and in the answers the relationship that I consider correct, complete the JSON only with the answer and nothing else:\n ['

description1 = ' { "question": { "Grumpier Old Men": "John and Max resolve to save their beloved bait shop from turning into an Italian restaurant, just as its new female owner catches Max\'s attention.", "Leaving Las Vegas": "Ben Sanderson, a Hollywood screenwriter who lost everything because of his alcoholism, arrives in Las Vegas to drink himself to death. There, he meets and forms an uneasy friendship and non-interference pact with prostitute Sera." }, '
description2 = ' { "question": { "Mortal Kombat": "MMA fighter Cole Young seeks out Earth\'s greatest champions in order to stand against the enemies of Outworld in a high stakes battle for the universe.", "Batman Forever": "Batman must battle former district attorney Harvey Dent, who is now Two-Face and Edward Nygma, The Riddler with help from an amorous psychologist and a young circus acrobat who becomes his sidekick, Robin." }, '
description3 = ' { "question": { "Wes Craven\'s New Nightmare": "A demonic force has chosen Freddy Krueger as its portal to the real world. Can Heather Langenkamp play the part of Nancy one last time and trap the evil trying to enter our world?", "Balto": "An outcast Husky risks his life with other sled dogs to prevent a deadly epidemic from ravaging Nome, Alaska." }, '
description4 = ' { "question": { "Grumpier Old Men": "John and Max resolve to save their beloved bait shop from turning into an Italian restaurant, just as its new female owner catches Max\'s attention.", "Mortal Kombat": "MMA fighter Cole Young seeks out Earth\'s greatest champions in order to stand against the enemies of Outworld in a high stakes battle for the universe.", "Batman Forever": "Batman must battle former district attorney Harvey Dent, who is now Two-Face and Edward Nygma, The Riddler with help from an amorous psychologist and a young circus acrobat who becomes his sidekick, Robin.", "Leaving Las Vegas": "Ben Sanderson, a Hollywood screenwriter who lost everything because of his alcoholism, arrives in Las Vegas to drink himself to death. There, he meets and forms an uneasy friendship and non-interference pact with prostitute Sera." }, '


keyword1 = ' { "question": { "Ed\'s Next Move": "boyfriend girlfriend breakup, boyfriend girlfriend relationship, rice, move to new york city, roommate roommate relationship", "Waiting to Exhale": "black american, friendship between women, husband wife relationship, betrayal, mother son relationship" }, '
keyword2 = ' { "question": { "Nadja": "vampire, female vampire, boxing practice, morgue, uncle nephew relationship", "Castle Freak": "castle, redemption, haunted by the past, monster, blind girl" }, '
keyword3 = ' { "question": { "Maze Runner: The Death Cure": "human experimentation, virus, post apocalypse, resistance movement, friendship", "Circle of Friends": "class differences, 1950s, love, small town, lust" }, '
keyword4 = ' { "question": { "Grumpier Old Men": "sequel, boat, lake, rivalry, minnesota", "Mortal Kombat": "based on video game, gore, graphic violence, mortal kombat, reboot", "Batman Forever": "bruce wayne character, batman character, wayne manor, villain team up, gotham city", "Leaving Las Vegas": "prostitute, falling in love with a prostitute, based on novel, alcoholism, las vegas nevada" }, '


actors1 = ' { "question": { "Toy Story": [ "Tom Hanks", "Tim Allen", "Don Rickles" ], "Apollo 13": [ "Tom Hanks", "Bill Paxton", "Kevin Bacon" ] }, '
actors2 = ' { "question": { "Batman Forever": [ "Val Kilmer", "Tommy Lee Jones", "Jim Carrey" ], "The Truman Show": [ "Jim Carrey", "Ed Harris", "Laura Linney" ] }, '
actors3 = ' { "question": { "Maze Runner: The Death Cure": [ "Dylan O\'Brien", "Ki Hong Lee", "Kaya Scodelario" ], "Circle of Friends": [ "Chris O\'Donnell", "Minnie Driver", "Geraldine O\'Rawe" ] }, '
actors4 = ' { "question": { "Heat": [ "Al Pacino", "Robert De Niro", "Val Kilmer" ], "Casino": [ "Robert De Niro", "Sharon Stone", "Joe Pesci" ], "Two Bits": [ "Al Pacino", "Mary Elizabeth Mastrantonio", "Jerry Barone" ], "Taxi Driver": [ "Robert De Niro", "Jodie Foster", "Cybill Shepherd" ] }, '


directors1 = ' { "question": { "Taxi Driver": [ "Martin Scorsese" ], "Casino": [ "Martin Scorsese" ] }, '
directors2 = ' { "question": { "Jurassic Park": [ "Steven Spielberg" ], "Schindler\'s List": [ "Steven Spielberg" ] }, '
directors3 = ' { "question": { "Maze Runner: The Death Cure": [ "Wes Ball" ], "Circle of Friends": [ "Pat O\'Connor" ] }, '
directors4 = ' { "question": { "Heat": [ "Michael Mann" ], "Reckless": [ "James Foley" ], "Two Bits": [ "James Foley" ], "The Last of the Mohicans": [ "Michael Mann" ] }, '


creators1 = ' { "question": { "Grumpier Old Men": [ "Mark Steven Johnson" ], "Big Bully": [ "Mark Steven Johnson" ] }, '
creators2 = ' { "question": { "Demolition Man": [ "Peter M. Lenkov", "Robert Reneau", "Daniel Waters" ], "Son in Law": [ "Patrick J. Clifton", "Susan McMartin", "Peter M. Lenkov" ] }, '
creators3 = ' { "question": { "Maze Runner: The Death Cure": [ "T.S. Nowlin", "James Dashner" ], "Circle of Friends": [ "Andrew Davies", "Maeve Binchy" ] }, '
creators4 = ' { "question": { "Heat": [ "Michael Mann" ], "Casino": [ "Nicholas Pileggi", "Martin Scorsese" ], "City Hall": [ "Ken Lipper", "Paul Schrader", "Nicholas Pileggi" ], "The Insider": [ "Michael Mann" ] }, '

def ai(text, temp=0):
    now = time()

    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    completion = client.chat.completions.create(
    model="local-model", # not used
    messages=[
        {
        "role": "system",
        "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful.",
        },
        {
        "role": "user",
        "content": text,
        }
    ],
    max_tokens=100,
    temperature=temp,
    stream=True
    )

    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    
    print(int(time() - now))

    return response

def call_ai(text, question):
    text += question
    print(text)
    response = ai(text)
    print(response)
    response = response.split(',')
    result = []
    for e in response:
        if "I do not have a sentence" in e or\
            "is not specified in the given information" in e or\
            "is no sentence" in e or\
            "is not clear what sentence" in e or\
            "is no answer provided" in e: continue
        else:
            if "answer" in e:
                e = e[10:]
            for sep in seps:
                aux = cort(e, sep)
                if type(aux) == list:
                    for f in aux:
                        result.append(f)
                elif aux: result.append(aux)

    return result

def include(movies, data, word):
    question = ' { "question": {'
    not_desc = True
    for m in movies:
        if data[m][word]:
            not_desc = False
            question +=  ' "'
            question += data[m]['name']
            question += '": "'
            question += data[m][word]
            question += '",'
    if not_desc: return None
    question = question[:len(question) - 1]
    question += ' }, "answer": '
    return question

def include2(movies, data, word):
    question = ' { "question": {'
    not_desc = True
    for m in movies:
        if data[m][word]:
            not_desc = False
            question +=  ' "'
            question += data[m]['name']
            question += '": [ '
            for p in data[m][word]:
                question += '"'
                question += p['name']
                question += '", '
            question = question[:len(question) - 2]
            question += ' ],'
    if not_desc: return None
    question = question[:len(question) - 1]
    question += ' }, "answer": '
    return question

def actors(movies, data, feel):
    answer1 = '"answer": "I ' + feel + ' Tom Hanks movies" }, \n'
    answer2 = '"answer": "I ' + feel + ' Jim Carrey movies" }, \n'
    answer3 = '"answer": "I do not have a sentence about the actors of movies" }, \n'
    answer4 = '"answer": [ "I ' + feel + ' Robert De Niro movies", "I ' + feel + ' Al Pacino movies" ] }, \n'
    text = init + actors1 + answer1  + actors2 + answer2 + actors3 + answer3 + actors4 + answer4

    question = include2(movies, data, 'actor')
    if not question: return None
    return call_ai(text, question)

def directors(movies, data, feel):
    answer1 = '"answer": "I ' + feel + ' Martin Scorsese movies" }, \n'
    answer2 = '"answer": "I ' + feel + ' Steven Spielberg movies" }, \n'
    answer3 = '"answer": "I do not have a sentence about the directors of movies" }, \n'
    answer4 = '"answer": [ "I ' + feel + ' Michael Mann movies", "I ' + feel + ' James Foley movies" ] }, \n'
    text = init + directors1 + answer1  + directors2 + answer2 + directors3 + answer3 + directors4 + answer4

    question = include2(movies, data, 'director')
    if not question: return None
    return call_ai(text, question)

def creators(movies, data, feel):
    answer1 = '"answer": "I ' + feel + ' Mark Steven Johnson movies" }, \n'
    answer2 = '"answer": "I ' + feel + ' Peter M. Lenkov movies" }, \n'
    answer3 = '"answer": "I do not have a sentence about the creators of movies" }, \n'
    answer4 = '"answer": [ "I ' + feel + ' Michael Mann movies", "I ' + feel + ' Nicholas Pileggi movies" ] }, \n'
    text = init + creators1 + answer1  + creators2 + answer2 + creators3 + answer3 + creators4 + answer4

    question = include2(movies, data, 'creator')
    if not question: return None
    return call_ai(text, question)

def descriptions(movies, data, feel):
    answer1 = '"answer": "I ' + feel + ' romance movies" }, \n'
    answer2 = '"answer": "I ' + feel + ' action movies" }, \n'
    answer3 = '"answer": "I do not have a sentence about the genre of movies" }, \n'
    answer4 = '"answer": "I ' + feel + ' romance movies", "I ' + feel + ' action movies" }, \n'
    text = init + description1 + answer1  + description2 + answer2 + description3 + answer3 + description4 + answer4
    
    question = include(movies, data, 'description')
    if not question: return None
    return call_ai(text, question)

def keywords(movies, data, feel):
    answer1 = '"answer": "I ' + feel + ' romance movies" }, \n'
    answer2 = '"answer": "I ' + feel + ' monsters movies" }, \n'
    answer3 = '"answer": "I do not have a sentence about the genre of movies" }, \n'
    answer4 = '"answer": "I ' + feel + ' romance movies", "I ' + feel + ' action movies" }, \n'
    text = init + keyword1 + answer1  + keyword2 + answer2 + keyword3 + answer3 + keyword4 + answer4
    
    question = include(movies, data, 'keywords')
    if not question: return None
    return call_ai(text, question)