#!/usr/bin/env python3
'''
Agent WebInfra 
Get informations from Web Server
'''

import sys,os


current_dir = os.path.basename(os.getcwd())
if current_dir == "agents":
    sys.path.append('../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')

import re, random
from furl import *
from urllib.parse import urlparse
import time, signal
from multiprocessing import Process
import stomp
import re
from daemonize import Daemonize
from os.path import basename
from libs.STOMP import STOMP_Connector
from libs.FIPA import FIPAMessage
from libs.Transport import Transport
import libs.Utils as utl
import libs.Target as target
import config as cf

from actions.webInfraAction import WebInfraAction

from libs.boot_agents import show_help
#from libs.boot_agents import startAgent

AGENT_NAME="AgentWebInfra"
AGENT_ID="5"

urlTarget = ''


def handler(signum, frame):
    print("Exiting of execution...", signum);
    mAction = WebInfraAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.deregisterAgent()
    sys.exit(0)


def runAgent():        
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    
    print("Loading %s...\n" % AGENT_NAME)

    toAgent = "All Agents"
    content = ("Register Agent (= (agent-name) (" + AGENT_NAME + "))\n")              
    reply_with = utl.id_generator()
    conversation_id = utl.id_gen()   
    mAction = WebInfraAction()
    mAgent = Transport()
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
                    mAction.add_avaiable_agent(agt_id)
                    break
            else:
                print(rcv)
    
    mAction = WebInfraAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    #request url base to check
    toAgent = "AgentTarget"
    ret = mAction.requestUrlBase(toAgent)
    mAction.receive_pkg(mAgent)
    
    #
        #mAction = Action()
    #mAgent = Transport()
    #mAction.set_mAgent(mAgent)
    #ret = mAction.sendHTTPHeaders()
    #mAction.receive_pkg(mAgent)
    
    

    
def startAgent(background=False):
    if background == True:
        pid = os.fork()
        if pid:
            p = basename(sys.argv[0])
            myname, file_extension = os.path.splitext(p)
            pidfile = '/tmp/%s.pid' % myname
            daemon = Daemonize(app=myname, pid=pidfile, action=runAgent)
            daemon.start()        
    else:
        runAgent()        
    
def main(args):
    if args[0] == "foreground":
        startAgent(background=False)
    else:
        if args[0] == "background":
            startAgent(background=True)
        else:
            show_help(__file__)
            exit    
    exit    
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_help(__file__)
    else:
        main(sys.argv[1:])
    