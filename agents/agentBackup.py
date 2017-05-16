#!/usr/bin/env python3
'''
Kurgan MultiAgent Framework 
http://www.kurgan.com.br/

Agent to check for backup and interesting files.

Author: Glaudson Ocampos - <glaudson@kurgan.com.br>
Created in August 09th, 2016.
Last Modified in January 13th, 2017.
'''

import sys, os

import random
import string
from multiprocessing import Process
import stomp
import signal, time
from daemonize import Daemonize
from os.path import basename

current_dir = os.path.basename(os.getcwd())
if current_dir == "agents":
    sys.path.append('../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')
#from libs.STOMP import STOMP_Connector
from libs.FIPA import FIPAMessage
import config as cf

AGENT_NAME="AgentBackup"
AGENT_ID="20"

conn = ''

class AgentBackup:
    url = ''
    port = ''
    conn = stomp.Connection()
    
    def readConfig(self, conf):
        print("Getting configurations..")
    
    def setURL(self, val): 
        self.url = val
    def getURL(self):
        return self.url
    
    def setPort(self, val):
        selt.port = val
    def getPort(self):
        return self.port
    
    def setConn(self, val):
        conn = val
    def getConn(self):
        return self.conn
    
    
class MyListener(stomp.ConnectionListener):
    running = 0

    def set_runnning(self, val):
        self.running = val
    def get_running(self):
        return self.running

    def on_error(self, headers, message):
        print('received an error "%s"' % message)
    def on_message(self, headers, message):
        #gen_fpm(message)
        
        if message == "AgentBackup":
           if self.running == 0:
              print("Running Attack to search backup and interesting files...")
#              conn.send(body='OK.. estou no ar!', destination='/queue/kurgan')
              msg = ("(tell\n"
              "\t:sender       AgentBackup\n"
              "\t:receiver     MainBoard\n"
              "\t:in-reply-to  msg777\n"
              "\t:ontology     KurganDict\n"
              "\t:language     Python\n"
              "\t:content      \"crawling(URL, Trying get backup and interesting files)\"\n"
              ")\n")
              
              send_message(msg)
              self.running = 1
              p = Process(target=crawling, args=('alvo',))
              p.start()
           else:
              msg="Agent in execution! Please Wait."
              send_message(msg)
              #conn.send(body='Agent in execution! Please Wait.', destination=cf.STOMP_DESTINATION)
              print("Ja executando o ataque de crawling....")
        else:
           print('%s' % message)


def send_message(msg):
    conn.send(body=msg, destination=cf.STOMP_TOPIC)
    
def receive_data_from_agents():
    ret = conn.receive_data()
    return ret
    
def handler(signum, frame):
    print("Stop execution...", signum);
    sys.exit(0)
    
    
def crawling(target):
    print("Crawling ataque.....");
    time.sleep(200000)

    
    
    
def main(args):
    if args[0] == "foreground":
        run()
    else:
        if args[0] == "background":
            run("on")
        else:
            show_help()
            exit    
    exit
    
    
    
def runAgent():
    signal.signal(signal.SIGINT, handler)
    global conn
    
    fpm = FIPAMessage()
    fpm.set_performative("subscribe")
    fpm.set_sender(AGENT_NAME)
    fpm.set_receiver("All Agents")
    content = ("Register Agent (= (agent-name) (" + AGENT_NAME + "))\n")
    fpm.set_content(content)
    fpm.set_reply_with(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5)))
    fpm.close_message()
    #print(fpm.get_message())
    
    conn = stomp.Connection()
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect(cf.STOMP_USERNAME, cf.STOMP_PASSWORD, wait=True)
    conn.subscribe(destination=cf.STOMP_TOPIC, id=AGENT_ID, ack='auto')
    conn.send(body=''.join(fpm.get_message()), destination=cf.STOMP_TOPIC)

    
    while True:
        time.sleep(2)
        #rcv = receive_data_from_agents()
        #if not rcv:
        #    print(rcv)

    conn.disconnect()

    
     
def show_help():
    print("Kurgan MultiAgent Framework version ", cf.VERSION)
    print("Usage: python3 agentBackup.py <background|foreground>")
    print("\nExample:\n")
    print("python3 agentBackup.py background")
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
            print("Agent Loaded.")
    else:
        runAgent()        

def main(args):
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
        main(sys.argv[1:])