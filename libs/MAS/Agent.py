'''
Vortex Artificial Intelligence
http://www.vortex-ai.com.br/

Kurgan AI - MultiAgent WEB Security Framework
http://www.kurgan.com.br/ 

Agent class.

Author: Glaudson Ocampos - <glaudson@vortex-ai.com.br>
Created in February 28, 2017.
'''

import os, sys

current_dir = os.path.basename(os.getcwd())
if current_dir == "Reconnaissance":
    sys.path.append('../../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')
    
from libs.Transport import Transport

class Agent(object):
    name = ''
    id = ''
    actions = []
    states = []
    observations = []
   
    transport = ''
    
    def __init__(self):
        self.transport = Transport()
        
    
    def set_name(self, val):
        self.name = val
    def get_name(self):
        return self.name

    def set_id(self, val):
        self.id = val
    def get_id(self):
        return self.id

    def add_action(self, val):
        self.actions.append(val)
    def remove_action(self,val):
        self.actions.remove(val)
    def get_actions(self):
        return self.actions
    
    def add_state(self, val):
        self.states.append(val)
    def remove_state(self,val):
        self.states.remove(val)
    def get_states(self):
        return self.states
    
    def add_observation(self, val):
        self.observations.append(val)
    def remove_observation(self,val):
        self.observations.remove(val)
    def get_observations(self):
        return self.observations
    

