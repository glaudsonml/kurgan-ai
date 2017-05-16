'''
POMDP - brute force login
'''
import os
import sys

current_dir = os.path.basename(os.getcwd())
if current_dir == "BruteForce":
    sys.path.append('../../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')
    
import libs.Utils as utl
import config as cf
#from libs.MAS.Agent import Agent
import numpy as np
from libs.extern.pomdp import *


POMDP_FILE="libs/POMDP/BruteForce/bruteforce.pomdp"
POLICY_FILE="libs/POMDP/BruteForce/bruteforce.policy"


class POMDP_BruteForce(object):
    actions = ['page_classifier', 'run_brute_force', 'run_spider']
    states = ['vulnerable', 'not_vulnerable']
    observations = ['vulnerable_brute_force', 'not_vulnerable_brute_force', 'not_not_vulnerable_brute_force']
    pomdp = ''
    policy = ''
    
    best_action = ''
    
    def set_best_action(self, val):
        self.best_action = val
    def get_best_action(self):
        return self.best_action
            
    def __init__(self):
        self.pomdp = cf.KURGAN_HOME + POMDP_FILE
        self.policy = cf.KURGAN_HOME + POLICY_FILE
        
    def run(self):
        #pomdp = POMDP(self.pomdp, self.policy, np.array([[0.65], [0.35]]))
        pomdp = POMDP(self.pomdp, self.policy, np.array([[0.60], [0.40]]))
        print("Running POMDP...")
        obs_idx = 0
        best_action_str = None
        while True:
            print('Round', obs_idx + 1)
            best_action_num, expected_reward = pomdp.get_best_action()
            best_action_str = pomdp.get_action_str(best_action_num)
            print('\t- action:         ', best_action_str)
            print('\t- expected reward:', expected_reward)
            if best_action_str != 'page_classifier':
                # We have a 'terminal' action 
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
        pomdp.update_belief(best_action_num, pomdp.get_obs_num('vulnerable_brute_force'))
        print('\t- belief:         ', np.round(pomdp.belief.flatten(), 3))
        self.best_action = best_action_str
        print("Finished POMDP.")

def main(args):
    bf = POMDP_BruteForce()
    bf.run()
    print("Best action: " + bf.get_best_action())
    

if __name__ == '__main__':
    main(sys.argv[1:])
