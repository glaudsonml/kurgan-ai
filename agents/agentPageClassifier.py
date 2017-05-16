#!/usr/bin/env python3
'''
Page Classifier Agent
'''

import sys,os
import validators
import re, random
from furl import *
from urllib.parse import urlparse
import time, signal
from multiprocessing import Process
import threading
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

from actions.pageclassifierAction import PageClassifierAction

AGENT_NAME="AgentPageClassifier"
AGENT_ID="4"


def agent_status():
    mAgent = Transport()
    mAction = PageClassifierAction()
    mAction.set_mAgent(mAgent)
    ret = mAction.requestInfo('request','All','agent-status','*')
    mAction.receive_pkg(mAgent)

def get_infra():
    mAgent = Transport()
    mAction = PageClassifierAction()
    mAction.set_mAgent(mAgent)
    toAgent = "AgentWebInfra"
    ret = mAction.requestInfo('request',toAgent,'agent-status','*')
    mAction.receive_pkg(mAgent)

def get_url_base():
    mAgent = Transport()
    mAction = PageClassifierAction()
    toAgent = "MasterAgent"
    mAction.set_mAgent(mAgent)
    ret = mAction.requestInfo('request',toAgent,'base-url-target','*')
    mAction.receive_pkg(mAgent)


def run_page_classifier():
    mAgent = Transport()
    mAction = PageClassifierAction()
    toAgent = "MasterAgent"
    mAction.set_mAgent(mAgent)
    ret = mAction.requestInfo('request',toAgent,'run-page-classifier','*')
    mAction.receive_pkg(mAgent)



def agent_quit():
    mAction = PageClassifierAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.deregister()
    sys.exit(0)

def handler(signum, frame):
    print("Exiting of execution...", signum);
    agent_quit()


def runAgent():
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    print("Loading " + AGENT_NAME + " ...\n")
    mAgent = Transport()
    mAction = PageClassifierAction()
    mAction.set_mAgent(mAgent)
    mAction.registerAgent()
    fm = FIPAMessage()
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
                    mAction.add_available_agent(agt_id)
                    break
            else:
                print(rcv)
    
    
    print("Available Agents: ", mAction.get_available_agents())
    
    mAgent = Transport()
    mAction = PageClassifierAction()
    mAction.set_mAgent(mAgent)
    mAction.cfp("page-classifier", "*")
    
    msg_id=[]
    while True:
        time.sleep(1)
        rcv = mAgent.receive_data_from_agents()
        if not len(rcv) == 0:
            fm.parse_pkg(rcv)
            match = re.search("message-id:(.\w+\-\w+)", rcv)
            if match:
                message_id = match.group(1).lstrip()
                if message_id in msg_id:
                    continue
                else:
                    msg_id.append(message_id)
                    print(rcv)
                    mAgent.zera_buff()
                    break
            else:
                print(rcv)

    p = Process(target=get_url_base())
    p.start()
    p.join(3)

    
    

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