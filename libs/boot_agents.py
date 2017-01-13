'''
Libraries used by agents
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

import config as cf

from libs.Transport import Transport


def show_help(agentFile):
    print("Kurgan MultiAgent Framework version ", cf.VERSION)
    print("Usage: python3 " + agentFile + " <background|foreground>")
    print("\nExample:\n")
    print("python3 " + agentFile + " background")
    exit(0) 
    

def handler(signum, frame, mAction):
    print("Exiting of execution...", signum);
    #mAction = WebInfraAction()
    mAgent = Transport()
    mAction.set_mAgent(mAgent)
    mAction.deregisterAgent()
    sys.exit(0)
