'''
Spider Agent Actions.
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

import libs.Spider as spider

AGENT_NAME="AgentSpider"
AGENT_ID="5"
ALL_AGENTS = "All"

urlTarget = ''
startTime = time.time()

class SpiderAction():
    mAgent = ''
    available_agents = []
    msg_id=[]
    baseUrlTarget = ''
    content = ''
    is_running = False
    total_links = 0
    links = []
    urlTarget = ''
    agent_can_run = True
    
    
    def set_agent_can_run(self, val):
        self.agent_can_run = val
    def get_agent_can_run(self):
        return self.agent_can_run
    
    def set_total_links(self, val):
        self.total_links = val
    def get_total_links(self):
        return self.total_links
    
    def add_links(self, val):
        self.links.append(val)
    def get_links(self):
        return self.links
    def zera_links(self):
        for i in self.links:
            del i
    
    def set_mAgent(self, val):
        self.mAgent = val

    def set_baseUrlTarget(self, val):
        self.baseUrlTarget = val
    def get_baseUrlTarget(self):
        return self.baseUrlTarget

    def set_UrlTarget(self, val):
        self.urlTarget = val
    def get_UrlTarget(self):
        return self.urlTarget
            
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
    
        #mAgent = MasterAgent()
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
    
    def requestInfo(self,performative, toAgent, reqfunction,values):
        content = ("Request Information (= (" + reqfunction + ") (" + values + "))\n")           
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()   
        
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
    
    
    def responseInfo(self,performative, toAgent, reply_to, reqfunction,values):
        content = ("Response (= (" + reqfunction + ") (" + values + "))\n")           
        conversation_id = utl.id_gen()   
        
        msg = self.mAgent.set_response_to_agent(performative,AGENT_NAME, toAgent, content, reply_to, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        return ret
    
    
    def registerUrl(self, url, toAgent):
        performative = "inform"
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()    
        content = ("Register urlTarget (= (url-target) (" + url + "))\n")              
    
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)

    
    def set_content(self, val):
        self.content = val
    def get_content(self):
        return self.content


    def run_spider_target(self, toAgent):
        self.total_links = 0
        self.links = []
        self.zera_links()

        print("Target is: " + self.baseUrlTarget)
        sp = spider.Spider()    
        if len(self.urlTarget) != 0:
            sp.set_baseUrl(self.urlTarget)
        else:
            sp.set_baseUrl(self.baseUrlTarget)            
            
        self.links = sp.run()
            
        body = ''
        total = 0
        for line in self.links:
            body += line + "\n"
            total += 1
            
        self.total_links = total 
          
        performative = "inform"
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()  
        content = ("Response From spider (= (run-spider) (" + body +  "))\n")  
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        self.is_running = False

        

    def runSpider(self, toAgent):
        if self.is_running is True:
            performative = "inform"
            reply_with = utl.id_generator()
            conversation_id = utl.id_gen()    
            body = "Spider in execution..."
            content = ("Response from Spider (= (run-spider) ("
                   + body + 
                   "))\n")              
    
            msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
            ret = self.mAgent.send_data_to_agent(msg)
            return ret
        else:
            self.zera_links()
            self.is_running = True
            p = Process(target=self.run_spider_target(toAgent))
            p.start()
            

        '''
        pid = os.fork()
        if pid == 0:
            print("Target is: " + self.baseUrlTarget)
            self.is_running = True
            sp = spider.Spider()    
            if len(self.urlTarget) != 0:
                sp.set_baseUrl(self.urlTarget)
            else:
                sp.set_baseUrl(self.baseUrlTarget)            
            self.links = sp.run()
            
            body = ''
            total = 0
            for line in self.links:
                body += line + "\n"
                total += 1
            
            self.total_links = total # fork is not update father process
          
            performative = "inform"
            reply_with = utl.id_generator()
            conversation_id = utl.id_gen()  
            content = ("Response page-classifier (= (run-spider) (" + body +  "))\n")  
            msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
            ret = self.mAgent.send_data_to_agent(msg)
            mypid = os.getpid(pid)
            os.kill(mypid, signal.SIGTERM)
        else:
            return
         '''   

    def agentStatus(self, toAgent):
        status = "UP"
        performative = "inform"
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()    

        uptime = time.time() - startTime
        content = ("Response agent-status (= (agent-status) ("
                   "AgentName: " +  AGENT_NAME + "\n"
                   "Agend_id: " + AGENT_ID + "\n" 
                   "Uptime: %0.2f " % uptime + "\n" 
                   "))\n")              
    
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        return ret


    def add_available_agent(self, agent_id):
        self.available_agents.append(agent_id)
    def del_available_agent(self, agent_id):
        for id in self.available_agents:
            if id == agent_id: 
                del self.available_agent[id]

    def get_available_agents(self):
        return self.available_agents

    def parse_action(self, fm):
        performative = fm.get_performative()
        action_function = fm.get_fname()
        description = fm.get_fdescription()
        values = fm.get_fvalues()
        toAgent = fm.get_sender()
        reply_with = fm.get_reply_with()
        
        mAgent = Transport()
        self.set_mAgent(mAgent)
        
        if action_function == "set-run-spider" and performative=='inform':
            if values == "True":
                self.agent_can_run = True
            else:
                if values == "False":
                    self.agent_can_run = False
                else:
                    self.agent_can_run = False #check this
           
        if action_function == "run-spider" and performative=='request':
            if self.agent_can_run is True:
                print ("Running Spider...")
                ret = self.runSpider(toAgent)
            else:
                values = "False"
                reply_to = reply_with
                self.responseInfo('inform', toAgent, reply_to, "run-spider", values)

        if action_function == "spider-get-total-links" and performative == "request":
            print ("Sending Total of Links to: " , toAgent)
            values = str(self.total_links)
            reply_to = reply_with
            self.responseInfo('inform', toAgent, reply_to, "spider-get-total-links", values)
            
        
        
        
        
        if action_function == "url-target":
            print ("Sending url-target to " , toAgent)
            ret = self.registerUrl(urlTarget, toAgent)
    
        if action_function == "agent-status":
            print ("Sending agent-up to " , toAgent)
            ret = self.agentStatus(toAgent)
    
        if action_function == "base-url-target":
            if performative == 'request':
                print ("Sending base-url-target to: " , toAgent)
                values = self.get_baseUrlTarget()
                reply_to = reply_with
                self.responseInfo('inform', toAgent, reply_to, "base-url-target", values)
            elif performative == 'inform':  
                self.baseUrlTarget = values





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



    