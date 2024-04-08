from agents import Belief
import google.generativeai as genai
import re
from fuzz import Fuzz
from numpy import average

with open('sim\\key.txt','r') as file:
    GOOGLE_API_KEY=file.read()
genai.configure(api_key=GOOGLE_API_KEY)

model=genai.GenerativeModel('gemini-pro')

class DifusseBelief(Belief):
    def __init__(self, likes, dislikes):
        self.likes=likes
        self.dislikes=dislikes
        self.liked_descrip=self._extract_(likes,'description')
        self.liked_actor=self._extract_(likes,'actor')
        self.chat_descrip=self._descrip()
        self.chat_actors=self._actors()
    
    def _extract_(self,movies,wich_extract:str):
        extract=[]
        for movie in movies:
            for m in movie:
                if wich_extract == 'actor':
                    for actor in m[wich_extract]:
                        extract.append(actor['name'])
                else:
                    if m[wich_extract] is not None:
                        extract.append(m[wich_extract])
                    else: continue
        return extract

    def _send_(self,chat,text):
        not_connect=True
        count=0
        while not_connect:
            try:
                response=chat.send_message(text)
                not_connect=False
            except:
                count+=1
                print(str(count)+'\n')
                if count==10:
                    print(ConnectionError())
                    break
        return (response if response is not None else ConnectionError)


    def _descrip(self):
        chat=model.start_chat(history=[])
        text='I am going to send you several descriptions in the following format:\n'
        text+='description: [description1]\n'
        text+='description: [description2]\n ...\n'
        text+='and I need you to respond:'
        text+='How much do you like the \"new_description\" given that you liked the previous ones?\n'
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
        text+='How much do you like the \"new_actor\" given that you liked the previous ones?\n'
        text+='new_actor: [new actor]'
        response=self._send_(chat,text)
        print(response.text)
    
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
        escaped=re.escape('[]')
        splited=re.split(f'[{escaped}]',response.text)
        value=int(splited[1] if len(splited[1])==1 else splited[1][0])  
        return value
    
    def calc_actor(self,actor,movies:dict):
        print('='*100)
        chat=self.chat_descrip
        text=''
        for m in self.liked_actor:
            text+='actor ['
            text+=m + ']\n'
        text+='new_actor: [' + actor['name'] + ']\n'
        text+=' Only responses of a number between 0 and 10. the number between []'
        print(text)

        response=self._send_(chat,text)

        print('='*100)
        print(response.text)
        escaped=re.escape('[]')
        splited=re.split(f'[{escaped}]',response.text)
        value=int(splited[1] if len(splited[1])==1 else splited[1][0])  
        return value



class DifusseAgent:
    def __init__(self, liked: dict, genome: dict, movies: dict):
        self.val = liked
        self.likes = [[movies[m] for m in liked if liked[m] == 1]]
        self.dislikes = [[movies[m] for m in liked if liked[m] == 0]]
        self.believes = DifusseBelief(self.likes, self.dislikes)
        self.actor_dict={}
        self.recommended = []
        self.inference=Fuzz()

    def perceive(self, recomended, movies):
        actor_rate=[]
        likes=[]
        for rec in recomended:
            actors=[]
            descrip=movies[rec]['description']
            if descrip is not None:
                descrip_value=self.believes.calc_descrip(descrip,movies)
            actor=movies[rec]['actor']
            if actor is not None:
                for act in actor:
                    actors.append(act)
                    actor_rate.append(self.believes.calc_actor(act,movies))
                actor_value=average(actor_rate)

            like_value=self.inference.calc(descrip_value,actor_value,True)
            if like_value >= 12:
                self.believes.liked_descrip.append(descrip)
                for act in actors:
                    try:
                        self.actor_dict[act['name']]+=1
                        if self.actor_dict[act['name']]==3:
                            self.believes.liked_actor.append(act['name'])
                    except:
                        self.actor_dict[act['name']]=0
            likes.append((like_value,rec))


        




