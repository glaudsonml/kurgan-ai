#!/usr/bin/env python3
'''
Agent Inform - Send inform to agents and show response.
'''

import sys,os
import validators
import re, random
from furl import *
from urllib.parse import urlparse
import time, signal
from multiprocessing import Process
import stomp
import re
from daemonize import Daemonize
from os.path import basename
from os.path import basename

current_dir = os.path.basename(os.getcwd())
if current_dir == "agents":
    sys.path.append('../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')
    
from libs.STOMP import STOMP_Connector
from libs.FIPA import FIPAMessage
from libs.Transport import Transport
import libs.Utils as utl
import config as cf

AGENT_NAME="AgentInform"
AGENT_ID="21"
ALL_AGENTS = "All"

class InformAction():
    mAgent = ''
    avaiable_agents = []
    msg_id=[]
    values = ''
    directive = ''
    
    def set_values(self, val):
        self.values = val
    def get_values(self):
        return self.values
    
    def set_directive(self, val):
        self.directive = val
    def get_directive(self):
        return self.directive
        
    def set_mAgent(self, val):
        self.mAgent = val
        
    def register(self):
        sender = AGENT_NAME
        toAgent = ALL_AGENTS
        content = ("Register Agent (= (agent-name) (" + AGENT_NAME + "))\n")              
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        msg = self.mAgent.set_data_to_agent("subscribe", sender, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

    def deregister(self):
        sender = AGENT_NAME
        performative = "subscribe"
        toAgent = ALL_AGENTS
        content = ("Deregister Agent (= (agent-name) (" + AGENT_NAME + "))\n")           
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        msg = self.mAgent.set_data_to_agent(performative, sender, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

    def sendInform(self, toAgent):
        sender = AGENT_NAME
        performative = "inform"
        content = ("Sending Information (= (" + self.directive + ") (" + self.values + "))\n")           
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        msg = self.mAgent.set_data_to_agent(performative, sender, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

        
    def parse_action(self, fm, mAgent):
        agent_quit()
        
    def receive_pkg(self, mAgent):
        fm = FIPAMessage()
        while True:
            time.sleep(1)
            rcv = mAgent.receive_data_from_agents()
            if not len(rcv) == 0:
                fm.parse_pkg(rcv)
                match = re.search("message-id:(.\w+\-\w+)", rcv)
                if match:
                    message_id = match.group(1).lstrip()
                    if message_id in self.msg_id:
                        continue
                    else:
                        self.msg_id.append(message_id)
                        mAgent.zera_buff()
                        receiver = fm.get_receiver()
                        if receiver == "All" or receiver == AGENT_NAME:
                            self.parse_action(fm, mAgent)
                            #break
                        else:
                            print(rcv)
                        #break
                        
                else:
                    print(rcv)
                    break




    def add_avaiable_agent(self, agent_id):
        self.avaiable_agents.append(agent_id)
    def del_avaiable_agent(self, agent_id):
        for id in self.avaiable_agents:
            if id == agent_id: 
                del self.avaiable_agent[id]

    def get_avaiable_agents(self):
        return self.avaiable_agents
    



def agent_quit():
    mAction = InformAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.deregister()
    sys.exit(0)

def handler(signum, frame):
    print("Exiting of execution...", signum);
    agent_quit()

def runAgent(toAgent, directive, values):
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    print("Loading " + AGENT_NAME + " ...\n")
    mAction = InformAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.register()
    fm = FIPAMessage()
    msg_id=[]
    agent_id=[]
    while True:
        time.sleep(1)
        rcv = mAgent.receive_data_from_agents()
        if not len(rcv) == 0:
            fm.parse_pkg(rcv)
            match = re.search("(agent-name(.)+)(\(\w+\))", rcv)
            if match:
                field = match.group(3).lstrip()
                match2 = re.search("\w+",field)
                if match2:
                    agt_id = match2.group(0)
                
                if agt_id in agent_id:
                    continue
                else:
                    print("agentID: ", agt_id)
                    agent_id.append(agt_id)
                    print(rcv)
                    mAction.add_avaiable_agent(agt_id)
                    break
            else:
                print(rcv)
    
    
    mAction = InformAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.set_directive(directive)
    mAction.set_values(values)
    ret = mAction.sendInform(toAgent)
    #mAction.receive_pkg(mAgent)
    print("Check now with Question!\n")
    time.sleep(2)
    agent_quit()
    

def show_help():
    print("Kurgan MultiAgent Framework version ", cf.VERSION)
    print("Usage: python3 " + __file__ + " <to_agent> <information>")
    print("\nExample:\n")
    print("python3 " + __file__ + " AgentTarget base-url-target http://www.kurgan.com.br/")
    print("python3 " + __file__ + " MasterAgent set-run-spider True")
    print("python3 " + __file__ + " MasterAgent set-run-brute-force False")
    exit(0) 


def main(args):
    toAgent = args[0]
    directive = args[1]
    values = args[2]
    runAgent(toAgent, directive, values)
    exit    
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_help()
    else:
        main(sys.argv[1:])