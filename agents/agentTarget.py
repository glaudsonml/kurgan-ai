#!/usr/bin/env python3
'''
Agent Target
'''

import sys,os
import re, random
from furl import *
from urllib.parse import urlparse
import time, signal
from multiprocessing import Process
import stomp
import re
from daemonize import Daemonize
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
import libs.Target as target
import config as cf

from actions.targetAction import TargetAction

AGENT_NAME="AgentTarget"
AGENT_ID="3"

urlTarget = ''


def handler(signum, frame):
    print("Exiting of execution...", signum);
    mAction = TargetAction()
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
    mAction = TargetAction()
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
    
    mAction = TargetAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.set_baseUrlTarget(urlTarget)
    ret = mAction.registerUrl(urlTarget, toAgent)
    #fm = FIPAMessage()
    mAction.receive_pkg(mAgent)
    
    mAction = TargetAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    ret = mAction.sendHTTPHeaders()
    mAction.receive_pkg(mAgent)
    
    

def show_help():
    print("Kurgan MultiAgent Framework version ", cf.VERSION)
    print("Usage: python3 " + __file__ + " <background|foreground> <url>")
    print("\nExample:\n")
    print("python3 " + __file__ + " background http://www.vortex-ai.com.br/")
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
    else:
        runAgent()        

def main(args):
    global urlTarget
    urlTarget = args[1]
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
    