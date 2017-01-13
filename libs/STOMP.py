'''
FIPA-ACL OVER STOMP PROTOCOL.

Author: Glaudson Ocampos - <glaudson@vortex-ai.com.br>
Created in July 28, 2016.
'''

#Regex to validation fipa-acl

import time
import sys, signal, os

import stomp

sys.path.append('../')
import config as cf

#class MyListener(stomp.ConnectionListener):
class MyListener():
    msg = []
    
    def __init__(self):
        self.msg = []
        
    def set_msg(self, val):
        self.msg = val
    def get_msg(self):
        return self.msg
    def zera(self):
       self.msg = ''
    
    def on_error(self, headers, message):
        self.msg = 'received an error "%s"' % headers + "msg: %s" % message 
        #print(self.msg)
        return self.msg
        
        
    def on_message(self, headers, message):
        message_id = 'message-id: %s\n' % headers['message-id']
        self.msg = message_id + message
        #print(self.msg)

    


class STOMP_Connector(object):
    username = cf.STOMP_USERNAME
    password = cf.STOMP_PASSWORD
    destination = cf.STOMP_TOPIC
    listener = stomp.ConnectionListener
    content = ''
    conn = stomp.Connection12
    id = ''
    
    def __init__(self):
        self.conn = stomp.Connection()
        self.listener = MyListener()
        
    def set_username(self, val):
        self.username = val
    def get_username(self):
        return self.username

    def set_password(self, val):
        self.password = val
    def get_password(self):
        return self.password

    def set_destination(self, val):
        self.destination = val
    def get_destination(self):
        return self.destination

    def set_listener(self, val):
        self.listener = val
    def get_listener(self):
        return self.listener    

    def set_content(self, val):
        self.content = val
    def get_content(self):
        return self.content 

    def set_id(self, val):
        self.id = val
    def get_id(self):
        return self.id

    def connect(self):
        self.conn.set_listener('', self.listener)
        self.conn.start()
        self.conn.connect(self.username, self.password, wait=True)
        self.conn.subscribe(destination= self.destination, id=self.id, ack='client')
    
    def send_data(self):
        #self.conn.subscribe(destination= self.destination, id=self.id, ack='client')
        self.conn.send(body=self.content, destination=self.destination)
        
    def send_ack(self, message_id):
        self.conn.set_listener('', self.listener)
        self.conn.start()
        self.conn.connect(self.username, self.password, wait=True)
        self.conn.subscribe(destination= self.destination, id=self.id, ack='client')
        self.conn.ack(id=message_id)
        
        
    def receive_data(self):
        msg = self.listener.get_msg()
        return msg
    
    def zera_buff(self):
        self.listener.zera()
    
    def disconnect(self):
        self.conn.disconnect()
