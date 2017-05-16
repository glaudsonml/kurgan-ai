#!/usr/bin/python3
'''
Kurgan Framework - AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@vortex-ai.com.br>

Created in May, 11th 2016.
Last modified in Fev, 25th 2016.
'''

import sys, os
import signal
from furl import *
import config as cf
from subprocess import check_output, Popen
from pathlib import Path
from os.path import basename
import subprocess
import config as cf
import time

PYTHON="/usr/bin/python3"

def run_apache_apollo(cmd=''):
    currDir = os.getcwd()
    argCMD = currDir  + cf.APACHE_APOLLO_CMD + " " + cmd 
    os.system(argCMD)
    
    
def get_pid(name):
    return check_output(["pidof"],name)
#
def load_agents():
    for i in cf.AGENTS_FILES:
        argCMD = ''
        print("Loading agent " + i)
        agentFile = cf.AGENTS_DIR + i + ".py"
        p = basename(agentFile)
        myname, file_extension = os.path.splitext(p)
        argCMD = '/usr/bin/python3 ' + agentFile + ' background '
        os.system(argCMD)
        time.sleep(3)

def status_agent(agentName):
    cmd = PYTHON + " agents/agentQuestion.py " + agentName + " agent-status"
    os.system(cmd)   
    
def start_infra():
    run_apache_apollo(cmd="start")
    
def stop_infra():
    run_apache_apollo(cmd="stop")
    
def restart_infra():
    run_apache_apollo(cmd="restart")

def restart_agents():
    stop_agent(all=True)
    time.sleep(1)
    load_agents()
    
def stop_agent(all=False, agent_name=''):
    if all==False:
        for i in cf.AGENTS_FILES:
            if i == agent_name:
                print("Stop agent: %s" % agent_name)
                st = "/tmp/" + agent_name + ".pid"
                f = open(st,'r')
                p = f.readline()
                pid = int(p)
                os.kill(pid, signal.SIGTERM)
                f.close
                os.remove(st) #Warning!
    else:
        for i in cf.AGENTS_FILES:
            agentFile = '/tmp/%s.pid' % i
            if os.path.exists(agentFile):
                print("Stop Agent: %s" % i)
                f = open(agentFile,'r')
                p = f.readline()
                pid = int(p)
                os.kill(pid, signal.SIGTERM)
                f.close
                os.remove(agentFile)
                
    
def show_help():
    print("Kurgan-Framework version ", cf.VERSION)
    print("Usage: python3 kurgan.py <options>\n")
    print("Option can be:\n")
    print("start infra\t\t\tStart Infrastructure to load agents and attack resources.")
    print("start <URL>\t\t\tStart Agents to attack URL.")
    print("stop <agent_name>\t\tStop One Agent. or all agents(stop framework).")
    print("stop all\t\t\tStop all agents(stop framework).")
    print("status <agent_name>\t\tStatus of one agent.")
    print("status All\t\t\tStatus of all agents.")
    print("\nExamples:\n")
    print("python3 " + __file__ + " start infra")
    print("python3 " + __file__ + " start agents")
    print("python3 " + __file__ + " stop agentBackup")
    print("python3 " + __file__ + " stop agents")
    exit(0)
        
def main(args):
    if args is None:
        show_help()
    else:
        if args[0] == "start":
            if args[1] == "infra":
                start_infra()
                return
            if args[1] == "agents":
                load_agents()
        if args[0] == "stop":
            if args[1] == "infra":
                stop_infra()
                return
            if args[1] == "agents":
                stop_agent(all=True)
            else:
                stop_agent(agent_name=args[1])
        if args[0] == "restart":
            if args[1] == "infra":
                restart_infra()
                return
        if args[0] == "restart":
            if args[1] == "agents":
                restart_agents()
                return
        if args[0] == "status":
            agentName = args[1]
            status_agent(agentName)
        

if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_help()
    else:
        main(sys.argv[1:])

