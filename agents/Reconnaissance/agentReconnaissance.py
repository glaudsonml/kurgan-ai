#!/usr/bin/env python3
'''
Vortex Artificial Intelligence
http://www.vortex-ai.com.br/

Kurgan AI - MultiAgent WEB Security Framework
http://www.kurgan.com.br/ 

Agent class.

Author: Glaudson Ocampos - <glaudson@vortex-ai.com.br>
Created in February 28, 2017.
'''

import os
import sys
#from os.path import basename

current_dir = os.path.basename(os.getcwd())
if current_dir == "Reconnaissance":
    sys.path.append('../../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')
    
import libs.Utils as utl
import config as cf
from libs.MAS.Agent import Agent
import numpy as np
from libs.extern.pomdp import *


POMDP_FILE="agents/Reconnaissance/reconnaissance.pomdp"
POLICY_FILE="agents/Reconnaissance/reconnaissance.policy"

#POMDP Values
actions = ['wait_cmd', 'get_whois', 'get_infos']
states = ['response_with_information', 'response_without_information']
observations = ['has_whois', 'has_infos','has_infos']


def loadAgent(agent):
    if type(agent) is not Agent:
        print("Wrong object type!")
        exit
        
    for a in actions:
        agent.add_action(a)
    
    for s in states:
        agent.add_state(s)
    
    for o in observations:
        agent.add_observation(o)
    
    

def runAgent():
    agent = Agent()
    loadAgent(agent)
    
    pomdp = POMDP(POMDP_FILE,POLICY_FILE, np.array([[0.65], [0.35]]))
    obs_idx = 0
    best_action_str = None
    #observations = ['hearDelete', 'hearSave', 'hearSave']
    while True:
        print('Round', obs_idx + 1)
        best_action_num, expected_reward = pomdp.get_best_action()
        best_action_str = pomdp.get_action_str(best_action_num)
        print('\t- action:         ', best_action_str)
        print('\t- expected reward:', expected_reward)
        if best_action_str != 'wait_cmd':
            # We have a 'terminal' action (either 'doSave' or 'doDelete')
            break
        else:
            # The action is 'ask': Provide our next observation.
            obs_str = observations[obs_idx]
            obs_idx += 1
            print('\t- obs given:      ', obs_str)
            obs_num = pomdp.get_obs_num(obs_str)
            pomdp.update_belief(best_action_num, obs_num)
            # Show beliefs
            print('\t- belief:         ', np.round(pomdp.belief.flatten(), 3))


    best_action_num, expected_reward = pomdp.get_best_action()
    pomdp.update_belief(best_action_num,
    pomdp.get_obs_num('has_whois')) # Observation doesn't affect this action.
    print('\t- belief:         ', np.round(pomdp.belief.flatten(), 3))
    
    

def main(args):
    runAgent()
    

if __name__ == '__main__':
    main(sys.argv[1:])
                  
