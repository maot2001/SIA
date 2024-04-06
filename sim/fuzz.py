import skfuzzy as fuzzy
import numpy as np 
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

class Fuzz:
    def __init__(self, view=False):
        val=self._obj()
        self.description=val[0]
        self.actor=val[1]
        self.like=val[2]
        self.rules=self._define_rules()

        if view:
            self.description.view()
            self.actor.view()
            self.like.view()
            print()



    def _obj(self):

        description = ctrl.Antecedent(np.arange(0,11,1),'description')
        actor = ctrl.Antecedent(np.arange(0,11,1),'actor')
        like = ctrl.Consequent(np.arange(0,16,1),'like')

        description.automf(3)
        actor.automf(3)
        like['little'] = fuzzy.trapmf(like.universe, [0, 0, 3, 7])
        like['medium'] = fuzzy.trapmf(like.universe, [0, 7, 8, 15])
        like['lot'] = fuzzy.trapmf(like.universe, [8, 12, 15, 15])

        return (description,actor,like)
    
    def _define_rules(self):
        rule1 = ctrl.Rule(self.description['poor'] | self.actor['poor'], self.like['little'])
        rule3 = ctrl.Rule(self.description['poor'] | self.actor['good'], self.like['medium'])
        rule4 = ctrl.Rule(self.description['good'] | self.actor['good'], self.like['lot'])
        rule9 = ctrl.Rule(self.description['average'] | self.actor['average'], self.like['medium'])

        return [rule1, rule3, rule4, rule9]
    
    def calc(self,description_value,actor_value, view=False):
        like_ctrl = ctrl.ControlSystem(self.rules)
        liked = ctrl.ControlSystemSimulation(like_ctrl)
        liked.inputs({'description':description_value,'actor':actor_value})
        liked.compute()
        if view:
            self.like.view(sim=liked)
            print(liked.output['like'])
        return liked.output['like']










