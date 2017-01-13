#!/usr/bin/python3
'''
Kurgan Framework - AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@vortex-ai.com.br>

Created in May, 11th 2016.
Last modified in Sep, 30th 2016.
'''

import sys, os
import signal
from furl import *
import config as cf
from subprocess import check_output
from pathlib import Path
from os.path import basename
import subprocess
import config as cf

def run_apache_apollo(cmd=''):
    argCMD = cf.APACHE_APOLLO + ' ' + cmd
    os.system(argCMD)
    
    
def get_pid(name):
    return check_output(["pidof"],name)
#
def load_agents(url):
#    agents = os.listdir(cf.AGENTS_DIR)
#    for i in agents:
    for i in cf.AGENTS:
        pid = os.fork()
        if pid:
            print("Loading agent %s" % i)
            agentFile = cf.AGENTS_DIR + i + ".py"
            p = basename(agentFile)
            myname, file_extension = os.path.splitext(p)
            if myname == "agentTarget":
                argCMD = '/usr/bin/python3 ' + agentFile + ' background ' + url
            else:
                argCMD = '/usr/bin/python3 ' + agentFile + ' background '
                
            os.system(argCMD)

def stop_agent(all=False, agent_name=''):
    if all==False:
        for i in cf.AGENTS:
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
        for i in cf.AGENTS:
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
    print("start <URL>\t\t\tStart Agents to attack URL.")
    print("stop <agent_name>\t\tStop One Agent. or all agents(stop framework).")
    print("stop all\t\t\tStop all agents(stop framework).")
    print("status <agent_name>\t\tStatus of one agent.")
    print("status all\t\t\tStatus of all agents.")
    print("\nExamples:\n")
    print("python3 kurgan.py start http://www.target.com.br/")
    print("python3 kurgan.py stop agentBackup")
    print("python3 kurgan.py stop all")
    exit(0)
        
def main(args):
    if args is None:
        show_help()
    else:
        if args[0] == "start":
            url = args[1]
            load_agents(url)
        if args[0] == "stop":
            if args[1] == "all":
                stop_agent(all=True)
            else:
                stop_agent(agent_name=args[1])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_help()
    else:
        main(sys.argv[1:])

