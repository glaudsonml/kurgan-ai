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

from libs.POMDPBruteForce import POMDP_BruteForce


AGENT_NAME="MasterAgent"
AGENT_ID="1"

ALL_AGENTS = "All"

class MasterAction():
    mAgent = ''
    available_agents = []
    msg_id=[]
    baseUrlTarget =  ''
    attacks = {}
    is_running_pomdp = False
    pageDetected = ''
    dataReturned = ''
    
    origAgent = ''
    origReplyWith = ''
    
    def __init__(self):
        self.attacks = {"Spider":True, "Crawling":False, "BruteForce":True}
    
    def set_mAgent(self, val):
        self.mAgent = val
    
    def set_baseUrlTarget(self, val):
        self.baseUrlTarget = val
    def get_baseUrlTarget(self):
        return self.baseUrlTarget
    
    def set_attacks(self, val):
        self.attacks.update(val)
    def get_attacks(self):
        return self.attacks
    
    def set_dataReturned(self, val):
        self.dataReturned = val
    def get_dataReturned(self):
        return self.dataReturned
    
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

    def informAgent(self,performative, toAgent,  reqfunction,values):
        content = ("Inform Agent (= (" + reqfunction + ") (" + values + "))\n")
        reply_with = utl.id_generator()           
        conversation_id = utl.id_gen()   
        
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        return ret


    
    def add_available_agent(self, agent_id):
        self.available_agents.append(agent_id)
        
    def del_available_agent(self, agent_id):
        for id in self.available_agents:
            if id == agent_id: 
                self.available_agents.remove(id)

    def get_available_agents(self):
        return self.available_agents

    def set_pageDetecter(self, val):
        self.pageDetected = val
    def get_pageDetected(self):
        rec = self.receive_pkg(self.mAgent)
        r = self.requestInfo('request', "AgentPageClassifier", "get-page-detected", "*")
        return self.pageDetected

    def check_page_returned(self, values):
        if values == 'FormLogin':
            self.pageDetected = values
            print("Page returned is:" + self.pageDetected)

            
    def ret_pomdp(self):
        pomdp = POMDP_BruteForce()
        pomdp.run()
        best_action = pomdp.get_best_action()
        print("Best action: " + best_action)
        
        if best_action == 'run_brute_force' and self.pageDetected == 'FormLogin':
            b = Process(target=self.requestInfo('request', "AgentBruteForce", "run-brute-force-headless", "*"))
            b.start()
            while b.is_alive() is True:
                time.sleep(1)
        
        #rec = self.receive_pkg(self.mAgent)
                 
    
    def pomdp_final_response(self, toAgent, reply_to, content):
        pomdp = POMDP_BruteForce()
        pomdp.run()
        best_action = pomdp.get_best_action()
        body = "POMDP Response:\n\n" + "Best-Action: " + best_action + "\n"
        body += "Data Returned: " + content 
        self.responseInfo('inform', toAgent, reply_to, "run-pomdp", body)
        self.is_running_pomdp = False

                 
    def run_pomdp_bf(self, toAgent, reply_with):
        p = Process(target=self.requestInfo('request', "AgentPageClassifier", "run-page-classifier-headless", "*"))
        p.start()
        while p.is_alive() is True:
            time.sleep(1)
        
        rec = self.receive_pkg(self.mAgent)

        


    def run_pomdp(self, toAgent, reply_with_orig):
        if self.is_running_pomdp is True:
            performative = "inform"
            reply_with = utl.id_generator()
            conversation_id = utl.id_gen()    
            body = "POMDP in execution..."
            content = ("Response from MasterAgent (= (run-pomdp) (" + body + "))\n")              
    
            msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
            ret = self.mAgent.send_data_to_agent(msg)
            return ret
        else:
            self.is_running_pomdp = True
            p = Process(target=self.run_pomdp_bf(toAgent, reply_with_orig))
            p.start()
            


    def parse_action(self, fm):
        performative = fm.get_performative()
        action_function = fm.get_fname()
        description = fm.get_fdescription()
        values = fm.get_fvalues()
        toAgent = fm.get_sender()
        reply_with = fm.get_reply_with()
        
        mAgent = Transport()
        self.set_mAgent(mAgent)
        
        #Dynamic programming?
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
                   'runInfoRetrieve':self.registerAgent(),
                   'runPOMDP':self.POMDP()
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
            if agent_name not in self.available_agents:
               print ("Adding agent: " , agent_name)
               self.add_available_agent(agent_name)

        if action_function == "agent-name" and performative == "subscribe" and description == "Deregister Agent":
            print ("Deregister agent: " , toAgent)
            agent_name = toAgent
            if agent_name in self.available_agents:
               print ("Removing agent: " , agent_name)
               self.del_available_agent(agent_name)

               
        if action_function == "agents-available":
            print ("Sending available-agents to: " , toAgent)
            all_agents = self.available_agents
            values = " ".join(str(x) for x in all_agents)
            reply_to = reply_with
            self.responseInfo('inform', toAgent, reply_to, "available-agent", values)
        
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
                
        if action_function == "set-run-spider":
            if performative == 'request':
                retval = ''
                if self.attacks["Spider"] == True:
                    retval = "True"
                else:
                    retval = "False"
                reply_to = reply_with
                self.responseInfo('inform', toAgent, reply_to, "set-run-spider", retval)
            elif performative == 'inform':
                if values == "True":
                    dados = {'Spider':True}
                    self.attacks.update(dados)
                    reply_to = reply_with
                    self.responseInfo('inform', 'AgentSpider', reply_to, "set-run-spider", "True") 
                if values == "False":  
                    dados = {'Spider':False}
                    self.attacks.update(dados)
                    reply_to = reply_with 
                    self.responseInfo('inform', 'AgentSpider', reply_to, "set-run-spider", "False")
            

        if action_function == "set-run-brute-force":
            if performative == 'request':
                retval = ''
                if self.attacks["BruteForce"] == True:
                    retval = "True"
                else:
                    retval = "False"
                reply_to = reply_with
                self.responseInfo('inform', toAgent, reply_to, "set-run-brute-force", retval)
            elif performative == 'inform':
                if values == "True":
                    dados = {'BruteForce':True}
                    self.attacks.update(dados)
                    reply_to = reply_with
                    self.responseInfo('inform', 'AgentBruteForce', reply_to, "set-run-brute-force", "True") 
                if values == "False":  
                    dados = {'BruteForce':False}
                    self.attacks.update(dados)
                    reply_to = reply_with 
                    self.responseInfo('inform', 'AgentBruteForce', reply_to, "set-run-brute-force", "False")


        #TODO: handle this
        #origAgent = ''
        #origReplywith = ''

        if action_function == "run-pomdp":
            if performative == 'inform':
                ret = self.run_pomdp(toAgent, reply_with)
            if performative == 'request':
                self.origAgent = toAgent
                self.origReplyWith = reply_with
                print("OrigAgent: " + self.origAgent)
                print("OrigReplywith: " + self.origReplyWith)
                ret = self.run_pomdp(toAgent, reply_with)

        if action_function == "get-page-detected":
            if performative == 'inform':
                self.pageDetected = values
                print("Page Detected is: " + self.pageDetected)
                if self.is_running_pomdp is True:
                    self.ret_pomdp()
                    
                

        if action_function == "run-page-classifier-headless":
            if performative == 'inform':
                self.requestInfo('request', "AgentPageClassifier", "get-page-detected", "*")
                
        if action_function == "run-brute-force-headless":
            if performative == 'inform':
                self.dataReturned = values
                #self.requestInfo('request', "AgentBruteForce", "brute-force-get-accounts", "*")
                print("Accounts Returned: " + self.dataReturned)
                if self.is_running_pomdp is True:
                    reply_to = reply_with
                    finalAgent = toAgent
                    finalReply = reply_with
                    print("FinalAgent: " + finalAgent)
                    print("FinalReply: " + finalReply)
                    self.pomdp_final_response(self.origAgent, self.origReplyWith, self.dataReturned) 
#                    self.pomdp_final_response(toAgent, reply_with, self.dataReturned)
                    

        
        #Error: loop?
        if action_function == "agent-status":
            match = re.search("AgentName:.(\w+)", values, re.DOTALL|re.MULTILINE)
            if match:
                agent_name = match.group(1).lstrip()
                if agent_name not in self.available_agents:
                    print ("Adding agent: " , agent_name)
                    self.add_available_agent(agent_name)



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
