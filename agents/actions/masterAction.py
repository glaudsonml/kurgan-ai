'''
Action take by agent
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


AGENT_NAME="MasterAgent"
AGENT_ID="1"

ALL_AGENTS = "All"

class MasterAction():
    mAgent = ''
    avaiable_agents = []
    msg_id=[]
    baseUrlTarget =  ''
     
    def set_mAgent(self, val):
        self.mAgent = val
    
    def set_baseUrlTarget(self, val):
        self.baseUrlTarget = val
    def get_baseUrlTarget(self):
        return self.baseUrlTarget
        
    def registerAgent(self):
        performative = "subscribe"
        toAgent = ALL_AGENTS
        content = ("Register Agent (= (agent-name) (" + AGENT_NAME + "))\n")              
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

    def deregister(self):
        performative = "subscribe"
        toAgent = ALL_AGENTS
        content = ("Deregister Agent (= (agent-name) (" + AGENT_NAME + "))\n")           
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
    
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

    def cfp(self,reqfunction,values):
        performative = "cfp"
        toAgent = ALL_AGENTS
        content = ("Call For Propose (= (" + reqfunction + ") (" + values + "))\n")           
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
    
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        
    def requestInfo(self,performative, toAgent,  reqfunction,values):
        content = ("Request Information (= (" + reqfunction + ") (" + values + "))\n")
        reply_with = utl.id_generator()           
        conversation_id = utl.id_gen()   
        
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        return ret
    
    def responseInfo(self,performative, toAgent, reply_to, reqfunction,values):
        content = ("Response (= (" + reqfunction + ") (" + values + "))\n")           
        conversation_id = utl.id_gen()   
        
        msg = self.mAgent.set_response_to_agent(performative,AGENT_NAME, toAgent, content, reply_to, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        return ret
    
    def add_avaiable_agent(self, agent_id):
        self.avaiable_agents.append(agent_id)
        
    def del_avaiable_agent(self, agent_id):
        for id in self.avaiable_agents:
            if id == agent_id: 
                self.avaiable_agents.remove(id)

    def get_avaiable_agents(self):
        return self.avaiable_agents

    def parse_action(self, fm):
        performative = fm.get_performative()
        action_function = fm.get_fname()
        description = fm.get_fdescription()
        values = fm.get_fvalues()
        toAgent = fm.get_sender()
        reply_with = fm.get_reply_with()
        
        mAgent = Transport()
        self.set_mAgent(mAgent)
        
        #Dynamic programming
        '''
        actions = {'registerAgent':self.registerAgent(), 
                   'deRegisterAgent':self.registerAgent(), 
                   'getStatusOfAgent':self.registerAgent(),
                   'setBaseUrlTarget':self.registerAgent(),
                   'setUrlTarget':self.registerAgent(),
                   'getWebInfra':self.registerAgent(), 
                   'runCrawling':self.registerAgent(), 
                   'runBackup':self.registerAgent(), 
                   'runSQLInjection':self.registerAgent(), 
                   'runBruteForceLogin':self.registerAgent(), 
                   'runXSS':self.registerAgent(), 
                   'runScanDBVuln':self.registerAgent(), 
                   'runXSRF':self.registerAgent(), 
                   'runXXE':self.registerAgent(), 
                   'runLFI':self.registerAgent(), 
                   'runRFI':self.registerAgent(), 
                   'runObjectInjection':self.registerAgent(),
                   'runRCE':self.registerAgent(), 
                   'runELInjection':self.registerAgent(), 
                   'runLDAPInjection':self.registerAgent(), 
                   'runXPathInjection':self.registerAgent(), 
                   'runFuzzer':self.registerAgent(), 
                   'runInfoRetrieve':self.registerAgent()
                   }


        States = {'CheckAgents':0, 
                  'GettingBaseUrlTarget':0, 
                  'GetingWebInfraInformations':0, 
                  'WaitingAgentResponse':0, 
                  'WaitingAgentStatus':0,
                  'WaitingAttackStatus':0,  
                  'AfterGetWebInfra':0, 
                  'AfterRunCrawling':0, 
                  'AchieveGoal':0, 
                  'AfterAchieveGoal':0 
                  }
        '''


        
        
        if action_function == "agent-name" and performative == "subscribe" and description == "Register Agent":
            print ("Register agent: " , toAgent)
            agent_name = toAgent
            if agent_name not in self.avaiable_agents:
               print ("Adding agent: " , agent_name)
               self.add_avaiable_agent(agent_name)

        if action_function == "agent-name" and performative == "subscribe" and description == "Deregister Agent":
            print ("Deregister agent: " , toAgent)
            agent_name = toAgent
            if agent_name in self.avaiable_agents:
               print ("Removing agent: " , agent_name)
               self.del_avaiable_agent(agent_name)

               
        if action_function == "avaiable-agents":
            print ("Sending avaiable-agents to: " , toAgent)
            all_agents = self.avaiable_agents
            values = " ".join(str(x) for x in all_agents)
            reply_to = reply_with
            self.responseInfo('inform', toAgent, reply_to, "avaiable-agent", values)
        
        if action_function == "url-target":
            print ("Setting base-url-target to: " , values)
            self.baseUrlTarget = values
        
        if action_function == "base-url-target":
            if performative == 'request':
                print ("Sending base-url-target to: " , toAgent)
                values = self.get_baseUrlTarget()
                reply_to = reply_with
                self.responseInfo('inform', toAgent, reply_to, "base-url-target", values)
            elif performative == 'inform':  
                self.baseUrlTarget = values
        
        if action_function == "base-url-target" and performative=='request':
            print ("Sending base-url-target to: " , values)
            self.baseUrlTarget = values
        
        
        #Error: loop?
        if action_function == "agent-status":
            match = re.search("AgentName:.(\w+)", values, re.DOTALL|re.MULTILINE)
            if match:
                agent_name = match.group(1).lstrip()
                if agent_name not in self.avaiable_agents:
                    print ("Adding agent: " , agent_name)
                    self.add_avaiable_agent(agent_name)



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
                        sender = fm.get_sender()
                        if receiver == ALL_AGENTS or receiver == AGENT_NAME:
                            if sender != AGENT_NAME:
                                self.parse_action(fm)
                            #break
                        else:
                            print(rcv)
                        #break
                        
                else:
                    print(rcv)
                    break
