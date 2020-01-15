## This file contains the definition of classes of model algorithms. To add a new algorithm, add a new subclass to
## model.py and give it a method advance
##
## Written by: Andrew Pensoneault
from abc import ABC, abstractmethod

class Model(ABC):
    ## Parent 
    def __init__(self, initial_conditions):
        self.initial_conditions = initial_conditions
        self.ens_num = initial_conditions.shape[1]
    
    def set_initial_conditions(self, initial_conditions):
        self.initial_conditions = initial_conditions
        self.ens_num = initial_conditions.shape[1]

    def advance(self):
        pass

class identity(Model):
    ## Identity Model 
    def __init__(self, initial_conditions):
        super().__init__(self,initial_conditions)

    def advance(self):
        return self.initial_conditions
