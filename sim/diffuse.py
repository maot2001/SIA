from .vect_agent import Belief
import google.generativeai as genai
import re
from .fuzz import Fuzz

with open('sim\\key.txt','r') as file:
    GOOGLE_API_KEY=file.read()
genai.configure(api_key=GOOGLE_API_KEY)

model=genai.GenerativeModel('gemini-pro')

class DifusseBelief(Belief):
    def __init__(self, likes, dislikes):
        """
        Initializes a DifusseBelief object with likes and dislikes lists.

        Args:
        - likes (list): A list of liked movies with descriptions, actors, and directors.
        - dislikes (list): A list of disliked movies with descriptions, actors, and directors.
        """
        self.likes=likes
        self.dislikes=dislikes
        self.liked_descrip=self._extract_(likes,'description')
        self.liked_actor=self._extract_(likes,'actor')
        self.liked_director=self._extract_(likes,'director')
        self.chat_descrip=self._descrip()
        self.chat_actors=self._actors()
    
    def _extract_(self,movies,wich_extract:str):
        """
        Extracts information (like actors, directors, or descriptions) from a list of movies.

        Args:
        - movies (list): A list of movies containing information to extract.
        - which_extract (str): Specifies what type of information to extract ('actor', 'director', or 'description').

        Returns:
        - list: A list of extracted information based on the specified type.
        """
        extract=[]
        for movie in movies:
            for m in movie:
                if wich_extract == 'actor':
                    for actor in m[wich_extract]:
                        extract.append(actor['name'])
                elif wich_extract == 'director':
                    for actor in m[wich_extract]:
                        extract.append(actor['name'])
                else:
                    if m[wich_extract] is not None:
                        extract.append(m[wich_extract])
                    else: continue
        return extract
    

    # This method attempts to send a message to a chat object and handles potential connection errors by retrying up to 10 times.
    # It returns the response from the chat if successful, or a ConnectionError if the maximum retry limit is reached.
    def _send_(self,chat,text):
        not_connect=True
        count=0
        while not_connect:
            try:
                response=chat.send_message(text)
                not_connect=False
            except Exception as e:
                count+=1
                print(e.message)
                print(str(count)+'\n')
                if count==10:
                    print("LImit of message")
                    break
        return (response if response is not None else ConnectionError)
    
    def _parse_(self,response,chat,text):
        parse=False

        while not parse:
            try:
                try:
                    value = int(response.text)
                    parse = True
                except:
                    try:
                        escaped=re.escape('**')
                        splited=re.split(f'[{escaped}]',response.text)
                        value=int(splited[2])  
                        parse=True
                    except:
                        escaped=re.escape('[]')
                        splited=re.split(f'[{escaped}]',response.text)
                        if len(splited[1]) > 2:
                            escaped = re.escape('/')
                            splited=re.split(f'[{escaped}]',splited[1])
                        value=int(splited[1] if len(splited)>2 else splited[0])  
                        parse=True
            except:
                response=self._send_(chat,text)
        
        return value

    # This method starts a conversation with the chat model to gather information about directors, descriptions, or actors,
    # depending on the called function. It prompts the user to respond to each provided item and then prints the model's response.
    # It returns the chat object for further use.
    def _directors(self):
        chat=model.start_chat(history=[])
        text='I am going to send you several directors in the following format:\n'
        text+='director: [director1]\n'
        text+='director: [director2]\n ...\n'
        text+='and I need you to respond:'
        text+='How much could I like the \"new_directors\" given that you liked the previous ones?\n'
        text+='new_directors: [new_director1, new_director2, ... ]'
        response=self._send_(chat,text)
        print(response.text)
        return chat

    def _descrip(self):
        chat=model.start_chat(history=[])
        text='I am going to send you several descriptions in the following format:\n'
        text+='description: [description1]\n'
        text+='description: [description2]\n ...\n'
        text+='and I need you to respond:'
        text+='How much could I like the \"new_description\" given that you liked the previous ones?\n'
        text+='new_description: [new description]'
        response=self._send_(chat,text)
        print(response.text)
        return chat
    
    def _actors(self):
        chat=model.start_chat(history=[])
        text='I am going to send you several actors in the following format:\n'
        text+='actor: [actor1]\n'
        text+='actor: [actor2]\n ...\n'
        text+='and I need you to respond:'
        text+='How much could I like the \"new_actors\" given that you liked the previous ones?\n'
        text+='new_actors: [new_actor1, new_actor2, ...]'
        response=self._send_(chat,text)
        print(response.text)

    
    # This method calculates the user's affinity for a given description, actor, or director using the chat model.
    # It displays descriptions, actors, or directors that the user has liked previously, along with the new item to evaluate.
    # It prompts the user to respond with a number between 0 and 10 to indicate their affinity with the new item.
    # Returns the affinity value as an integer.
    def calc_descrip(self,description,movies:dict):
        print('='*100)
        chat=self.chat_descrip
        text=''
        for d in self.liked_descrip:
            text+='description ['
            text+=d + ']\n'
        text+='new description: [' + description + ']\n'
        text+=' Only responses of a number between 0 and 10. the number between []'
        print(text)
        
        response=self._send_(chat,text)

        print('='*100)
        print(response.text)
        value = self._parse_(response,chat,text) 
        return value
    
    def calc_actor(self,actor,movies:dict):
        print('='*100)
        chat=self.chat_descrip
        text=''
        for m in self.liked_actor:
            text+='actor ['
            text+=m + ']\n'
        text+='new_actors: [' 
        for a in actor:
            text += a['name'] + ', '
        text = text[:len(text)-2]
        text += ']\n'
        text+=' Only responses of a number between 0 and 10. the number between []'
        print('actor')

        response=self._send_(chat,text)

        print('='*100)
        print(response.text)
        value = self._parse_(response,chat,text) 

        return value
    
    def calc_director(self,director,movies:dict):
        print('='*100)
        chat=self.chat_descrip
        text=''
        for m in self.liked_director:
            text+='director ['
            text+=m + ']\n'
        text+='new_directors: [' 
        for d in director:
            text += d['name'] + ', '
        text = text[:len(text)-2]
        text += ']\n'
        text+=' Only responses of a number between 0 and 10. the number between []'
        print('director')

        response=self._send_(chat,text)

        print('='*100)
        print(response.text)
        value = self._parse_(response,chat,text) 
 
        return value


# The DifusseAgent class represents an agent that recommends and evaluates movies based on user preferences.
# It initializes with user likes, genome information, and movie data, and can perceive recommendations to take actions.
# The perceive method evaluates recommended movies using fuzzy logic and updates the agent's beliefs accordingly.
# The action method processes the evaluation results and updates the agent's liked descriptions, actors, and directors based on like values.
class DifusseAgent:
    def __init__(self, liked: dict, movies: dict):
        """
        Initializes a DifusseAgent object with user likes, genome information, and movie data.

        Args:
        - liked (dict): A dictionary representing user likes for movies.
        - genome (dict): A dictionary representing genome information.
        - movies (dict): A dictionary containing movie information.
        """
        self.val = liked
        self.likes = [[movies[m] for m in liked if liked[m] == 1]]
        self.dislikes = [[movies[m] for m in liked if liked[m] == 0]]
        self.believes = DifusseBelief(self.likes, self.dislikes)
        self.actor_dict={}
        self.director_dict={}
        self.recommended_like = []
        self.inference=Fuzz()

    def perceive(self, recomended, movies):
        for rec in recomended:
            
            descrip=movies[rec]['description']
            if descrip:
                descrip_value=self.believes.calc_descrip(descrip,movies)
            else:
                descrip_value=5

            actor=movies[rec]['actor']
            if actor:
                actor_value=self.believes.calc_actor(actor,movies)
            else:
                actor_value=5

            director=movies[rec]['director']
            if director:
                director_value=self.believes.calc_director(director,movies)
            else:
                director_value=5

            like_value=self.inference.calc(descrip_value,actor_value,director_value)
            self.action(like_value,rec)

    def action(self,like_value,movie):

        if like_value >= 9 and like_value < 12:
            
            if like_value >= 11:
                self.recommended_like.append(movie)
            """if descrip is not None:
                self.believes.liked_descrip.append(descrip)
            for act in actors:
                try:
                    self.actor_dict[act['name']]+=1
                    if self.actor_dict[act['name']]==3:
                        self.believes.liked_actor.append(act['name'])
                except:
                    self.actor_dict[act['name']]=0
            try:
                self.director_dict[direct['name']]+=1
                if self.director_dict[act['name']]==3:
                    self.believes.liked_director.append(direct['name'])
            except:
                self.director_dict[direct['name']]=0"""

        if like_value >= 12:
            """if descrip is not None:
                self.believes.liked_descrip.append(descrip)
            for act in actors:
                self.believes.liked_actor.append(act['name'])
            self.believes.liked_director.append(direct['name'])"""
            self.recommended_like.append(movie)



        




