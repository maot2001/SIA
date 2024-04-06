from agents import Belief
import google.generativeai as genai

with open('sim\\key.txt','r') as file:
    GOOGLE_API_KEY=file.read()
genai.configure(api_key=GOOGLE_API_KEY)

model=genai.GenerativeModel('gemini-pro')

class DifusseBelief(Belief):
    def __init__(self, likes, dislikes):
        self.likes=likes
        self.dislikes=dislikes
        self.chat_descrip=self._descrip()

    def _descrip(self):
        chat=model.start_chat(history=[])
        text='I am going to send you several descriptions in the following format:\n'
        text+='description: [description1]\n'
        text+='description: [description2]\n ...\n'
        text+='and I need you to respond:'
        text+='new_description: [new description]'
        text+='How much do you like the \"new_description\" given that you liked the previous ones?'
        response=chat.send_message(text)
        print(response.text)
        return chat
    
    def calc_descrip(self,description,movies:dict):
        print('='*100)
        chat=self.chat_descrip
        text=''
        for movies in self.likes:
            for m in movies:
                d=m['description']
                if d is not None:
                    text+='description ['
                    text+=d + ']\n'
                else: continue
        text+='new description: [' + description + ']\n'
        text+=' Only responses of a number between 0 and 10. the number between []'
        print(text)
        print('='*100)
        response=chat.send_message(text)
        print(response.text)
        splited=response.text.replace('[',"").replace(']',"")
        value=int(splited)
        return value



class DifusseAgent:
    def __init__(self, liked: dict, genome: dict, movies: dict):
        self.val = liked
        self.likes = [[movies[m] for m in liked if liked[m] == 1]]
        self.dislikes = [[movies[m] for m in liked if liked[m] == 0]]
        self.believes = DifusseBelief(self.likes, self.dislikes)
        self.recommended = {}

    def perceive(self, recomended, movies):
        for rec in recomended:
            d=movies[rec]['description']
            if d is not None:
                value=self.believes.calc_descrip(d,movies)
            else:
                continue
        




