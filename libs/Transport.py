import sys,os
import re, random
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
import libs.Utils as utl
import libs.Target as target
import config as cf


class Transport():
    cstomp = ''
    
    def __init__(self):
        self.cstomp = STOMP_Connector()

    def set_data_to_agent(self,performative,sender,toAgent,content,reply_with, conversation_id):
        fpm = FIPAMessage()
        fpm.set_performative(performative)
        fpm.set_sender(sender)
        fpm.set_receiver(toAgent)
        fpm.set_reply_with(reply_with)
        fpm.set_conversation_id(conversation_id)
        fpm.set_content(content)
        fpm.close_message()
        return fpm.get_message()

    def set_response_to_agent(self, performative, sender, toAgent, content, reply_to, conversation_id):
        fpm = FIPAMessage()
        fpm.set_performative(performative)
        fpm.set_sender(sender)
        fpm.set_receiver(toAgent)
        fpm.set_reply_to(reply_to)
        fpm.set_conversation_id(conversation_id)
        fpm.set_content(content)
        fpm.close_message()
        return fpm.get_message()
    
        
    def send_data_to_agent(self,msg):
        self.cstomp.set_content(msg)
        #self.cstomp.set_id(AGENT_ID)
        self.cstomp.connect()
        self.cstomp.send_data()
        ret = self.cstomp.receive_data()
        return ret

    def receive_data_from_agents(self):
        ret = self.cstomp.receive_data()
        return ret

    def send_ack(self, message_id):
        self.cstomp.send_ack(message_id)
    
    def zera_buff(self):
        self.cstomp.zera_buff()
    
    def send_disconnect(self):
        self.cstomp.disconnect()
