#!/usr/bin/env python3
'''
Agent Board - only print messages switched by agents.
It's possible to log then.
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

AGENT_NAME="AgentBoard"
AGENT_ID="4"

class BoardAction():
    mAgent = ''
    avaiable_agents = []
        
    def set_mAgent(self, val):
        self.mAgent = val
        
    def register(self):
        sender = AGENT_NAME
        toAgent = "All Agents"
        content = ("Register Agent (= (agent-name) (" + AGENT_NAME + "))\n")              
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        msg = self.mAgent.set_data_to_agent("subscribe", sender, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

    def deregister(self):
        sender = AGENT_NAME
        performative = "inform"
        toAgent = "All Agents"
        content = ("Deregister Agent (= (agent-name) (" + AGENT_NAME + "))\n")           
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        msg = self.mAgent.set_data_to_agent(performative, sender, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

    def showAgents(self):
        sender = AGENT_NAME
        performative = "request"
        toAgent = "MasterAgent"
        content = ("Request AvaiableAgents (= (avaiable-agents) (*))\n")           
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        msg = self.mAgent.set_data_to_agent(performative, sender, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)


    def add_avaiable_agent(self, agent_id):
        self.avaiable_agents.append(agent_id)
    def del_avaiable_agent(self, agent_id):
        for id in self.avaiable_agents:
            if id == agent_id: 
                del self.avaiable_agent[id]

    def get_avaiable_agents(self):
        return self.avaiable_agents
    

def handler(signum, frame):
    print("Exiting of execution...", signum);
    mAction = BoardAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.deregister()
    sys.exit(0)


def runAgent():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    print("Loading " + AGENT_NAME + " ...\n")
    mAction = BoardAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.register()
    fm = FIPAMessage()
    msg_id=[]
    while True:
        time.sleep(1)
        rcv = mAgent.receive_data_from_agents()
        if not len(rcv) == 0:
            match = re.search("message-id:(.\w+\-\w+)", rcv)
            if match:
                message_id = match.group(1).lstrip()
                if message_id in msg_id:
                    continue
                else:
                    msg_id.append(message_id)
                    fm.parse_pkg(rcv)
                    print(rcv)
                    mAgent.zera_buff()
            else:
                print(rcv)
    
    



def show_help():
    print("Kurgan MultiAgent Framework version ", cf.VERSION)
    print("Usage: python3 " + __file__ + " <background|foreground>")
    print("\nExample:\n")
    print("python3 " + __file__ + " background")
    exit(0) 

def run(background=False):
    if background == True:
        pid = os.fork()
        if pid:
            p = basename(sys.argv[0])
            myname, file_extension = os.path.splitext(p)
            pidfile = '/tmp/%s.pid' % myname
            daemon = Daemonize(app=myname, pid=pidfile, action=runAgent)
            daemon.start()        
            print("Agent Loaded.")
    else:
        runAgent()        

def main(args):
    if args[0] == "foreground":
        run(background=False)
    else:
        if args[0] == "background":
            run(background=True)
        else:
            show_help()
            exit    
    exit    
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_help()
    else:
        main(sys.argv[1:])