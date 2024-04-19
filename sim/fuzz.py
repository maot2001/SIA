import skfuzzy as fuzzy
import numpy as np 
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

class Fuzz:
    def __init__(self, view=False):
        val=self._obj()
        self.description=val[0]
        self.actor=val[1]
        self.director=val[2]
        self.like=val[3]
        self.rules=self._define_rules()

        if view:
            self.description.view()
            self.actor.view()
            self.like.view()
            print()



    def _obj(self):

        description = ctrl.Antecedent(np.arange(0,11,1),'description')
        actor = ctrl.Antecedent(np.arange(0,11,1),'actor')
        director = ctrl.Antecedent(np.arange(0,11,1),'director')
        like = ctrl.Consequent(np.arange(0,16,1),'like')

        description.automf(3)
        director.automf(3)
        actor.automf(3)
        like['poor'] = fuzzy.trapmf(like.universe, [0, 0, 2, 4])
        like['little'] = fuzzy.trapmf(like.universe, [3, 5, 6, 8])
        like['medium'] = fuzzy.trapmf(like.universe, [5, 7, 8, 11])
        like['decent'] = fuzzy.trapmf(like.universe, [8, 10, 11, 13])
        like['lot'] = fuzzy.trapmf(like.universe, [12, 14, 15, 15])

        return (description,actor,director,like)
    
# The rules in the _define_rules method establish relationships between movie features (description, actors, directors)
# and user preference (represented by terms like "poor", "average", "good", "lot", "medium", "decent", "little").
# These rules aim to associate specific combinations of quality in description, actors, and directors with user preference levels,
# thereby helping the system to evaluate and recommend movies more accurately based on user preferences.

    def _define_rules(self):

        rule1 = ctrl.Rule(self.description['poor'] & self.actor['poor'] & self.director['poor'], self.like['poor'])
        rule2 = ctrl.Rule(self.description['poor'] & self.actor['poor'] & self.director['average'], self.like['poor'])
        rule3 = ctrl.Rule(self.description['good'] & self.actor['good'] & self.director['good'], self.like['lot'])
        rule4 = ctrl.Rule(self.description['good'] & self.actor['good'] & self.director['average'], self.like['lot'])
        rule5 = ctrl.Rule(self.description['average'] & self.actor['average'] & self.director['average'], self.like['medium'])


        rule7= ctrl.Rule(self.actor['good'] & (self.description['average'] | self.director['average']) | 
                        self.description['good'] & (self.director['average'] | self.actor['average']),self.like['decent'])

        rule8 = ctrl.Rule(self.director['good'] & self.actor['good'] & self.description['average'],self.like['decent'])

        rule9 = ctrl.Rule(self.director['good'] & self.actor['poor'] & self.description['poor'],self.like['little'])


        rule10 = ctrl.Rule(self.actor['poor'] & (self.description['average'] | self.director['average']) | 
                        self.description['poor'] & (self.director['average'] | self.actor['average']),self.like['little'])


        rule11 = ctrl.Rule((self.description['average'] & (self.actor['good'] | self.director['good'])) | 
                        (self.actor['average'] & (self.description['good'] | self.director['good'])) | 
                        (self.director['average'] & (self.description['good'] | self.actor['good'])), self.like['decent'])

        rule12 = ctrl.Rule((self.description['average'] & (self.actor['poor'] | self.director['poor'])) | 
                        (self.actor['average'] & (self.description['poor'] | self.director['poor'])) | 
                        (self.director['average'] & (self.description['poor'] | self.actor['poor'])), self.like['little'])


        return [rule1, rule2, rule3, rule4, rule5,rule7,rule8,rule9,rule10,rule11,rule12]
    
    def calc(self,description_value,actor_value,director_value, view=False):
        """
        Calculates the preference value based on description, actor, and director values using a control system.

        Args:
        - description_value (int): The preference value for the movie description (between 0 and 10).
        - actor_value (int): The preference value for the movie actor (between 0 and 10).
        - director_value (int): The preference value for the movie director (between 0 and 10).
        - view (bool): Whether to display the control system view and the calculated preference value (default is False).

        Returns:
        - float: The calculated preference value based on the control system.
        """
        like_ctrl = ctrl.ControlSystem(self.rules)
        liked = ctrl.ControlSystemSimulation(like_ctrl)
        liked.inputs({'description':description_value,'actor':actor_value,'director':director_value})
        liked.compute()
        if view:
            self.like.view(sim=liked)
            print(liked.output['like'])
        return liked.output['like']










