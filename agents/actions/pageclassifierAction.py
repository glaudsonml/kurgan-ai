'''
Page Classifier Actions.
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

from libs.PageClassifier import PageClassifier
from libs.PageFormClassifier import PageFormClassifier

AGENT_NAME="AgentPageClassifier"
AGENT_ID="4"
ALL_AGENTS = "All"


startTime = time.time()

class PageClassifierAction():
    mAgent = ''
    available_agents = []
    msg_id=[]
    baseUrlTarget = ''
    content = ''
    urlTarget = '' 
    pageDetected = ''
    is_running_pc = False
    
    def __init__(self):
        self.urlTarget = ''
        
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

    def set_PageDetect(self, val):
        self.pageDetected = val
    def get_PageDetect(self):
        return self.pageDetected


            
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

    def run_pc(self, toAgent):
        pc = PageClassifier()
        
        if len(self.urlTarget) != 0:
            pc.set_url(self.urlTarget)
        else:
            pc.set_url(self.baseUrlTarget)
            
        body = 'Checking url: ' + pc.get_url() + '\n'
        retauth = pc.checkIfAuthForm()
        body = body + 'Page is Authentication Form Page: {0:.0f}%'.format(retauth) + '\n'
        retstatic = pc.checkIfStatic()
        
        body = body + 'Page is Static HTML Page: {0:.0f}%'.format(retstatic) + "\n" 
        retforgotten_password = pc.checkIfForgottenPassword()
        body = body + 'Page is Forgotten Password Page: {0:.0f}%'.format(retforgotten_password) + "\n"
        
        if (retauth > retstatic) and (retauth > retforgotten_password):
            self.pageDetected = "FormLogin"
        if (retauth < retstatic) and (retstatic > retforgotten_password):
            self.pageDetected = "Static"
        if (retauth < retforgotten_password) and (retstatic < retforgotten_password):
            self.pageDetected = "FormReset" 
        
        performative = "inform"
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()    

        uptime = time.time() - startTime
        content = ("Response page-classifier (= (run-page-classifier) (" + body + "))\n")              
    
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        self.is_running_pc = False
        return ret

    def run_pageClassifier(self, toAgent):
        if self.is_running_pc is True:
            performative = "inform"
            reply_with = utl.id_generator()
            conversation_id = utl.id_gen()    
            body = "Page Classifier in execution..."
            content = ("Response from PageClassifier (= (run-page-classifier) (" + body + "))\n")              
    
            msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
            ret = self.mAgent.send_data_to_agent(msg)
            return ret
        else:
            self.is_running_pc = True
            p = Process(target=self.run_pc(toAgent))
            p.start()
            


    def run_pc_headless(self, toAgent):
        pc = PageFormClassifier()
        
        if len(self.urlTarget) != 0:
            pc.set_url(self.urlTarget)
        else:
            pc.set_url(self.baseUrlTarget)
            
        body = 'Checking url: ' + pc.get_url() + '\n'
        pc.get_page()
        pc.run()
        is_authform = pc.get_isAuthform()
        if is_authform is True:
            self.pageDetected = "FormLogin"
            body = body + 'Page is Authentication Form Page:' + '{:.0%}'.format(float(pc.get_Accuracy())) + '\n'
            print("It is Authentication Form Page: " +  '{:.0%}'.format(float(pc.get_Accuracy())))
        else:
            body = body + 'Page is not Authentication Form Page:' + '{:.0%}'.format(float(pc.get_Accuracy())) + '\n'
            self.pageDetected = "NotFormLogin"
            print("It is not Authentication Form Page: " + '{:.0%}'.format(float(pc.get_Accuracy())))

        
        performative = "inform"
        reply_with = utl.id_generator()
        conversation_id = utl.id_gen()    

        uptime = time.time() - startTime
        content = ("Response page-classifier-headless (= (run-page-classifier-headless) (" + body + "))\n")              
    
        msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
        ret = self.mAgent.send_data_to_agent(msg)
        self.is_running_pc = False
        return ret



    def run_pageClassifierHeadless(self, toAgent):
        if self.is_running_pc is True:
            performative = "inform"
            reply_with = utl.id_generator()
            conversation_id = utl.id_gen()    
            body = "Page Classifier Headless in execution..."
            content = ("Response from PageClassifierHeadless (= (run-page-classifier-headless) (" + body + "))\n")              
    
            msg = self.mAgent.set_data_to_agent(performative,AGENT_NAME, toAgent, content, reply_with, conversation_id)
            ret = self.mAgent.send_data_to_agent(msg)
            return ret
        else:
            self.is_running_pc = True
            p = Process(target=self.run_pc_headless(toAgent))
            p.start()

        

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
           
        if action_function == "run-page-classifier" and performative=='request':
            ret = self.run_pageClassifier(toAgent)
        
        if action_function == "run-page-classifier" and performative=='inform':
            ret = self.run_pageClassifier(toAgent)
        
        if action_function == "run-page-classifier-headless" and performative=='request':
            ret = self.run_pageClassifierHeadless(toAgent)
        
        if action_function == "run-page-classifier-headless" and performative=='inform':
            ret = self.run_pageClassifierHeadless(toAgent)
        
        
        '''
        if action_function == "run-page-classifier" and performative=='inform':
            if values == "True":
                print ("Running Page Classifier in " , values)
                ret = self.XXXXrunSpider(toAgent)
            else:
                print ("Value to run spider " , values)
        '''
        if action_function == "url-target":
            if performative == 'request':
                values = self.get_UrlTarget()
                reply_to = reply_with
                self.responseInfo('inform', toAgent, reply_to, "url-target", values)
            elif performative == 'inform':  
                self.urlTarget = values
                
    
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

        if action_function == "get-page-detected":
            if performative == 'request':
                print ("Sending Page Detected to: " , toAgent)
                values = self.get_PageDetect()
                reply_to = reply_with
                self.responseInfo('inform', toAgent, reply_to, "get-page-detected", values)





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
                            continue
                            #print(rcv)
                        #break
                        
                else:
                    print(rcv)
                    break



    