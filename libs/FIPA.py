'''
Vortex Artificial Intelligence
http://www.vortex-ai.com.br/

Kurgan MultiAgent Framework 

FIPA-ACL for communicaton between agents.

Author: Glaudson Ocampos - <glaudson.ml@gmail.com>
Created in 09th August, 2016.

'''

import re
import io

#More informations:
#http://jmvidal.cse.sc.edu/talks/agentcommunication/performatives.html
FIPA_performative = ['accept-proposal','agree','cancel','cfp','confirm','disconfirm','failure','inform','inform-if','inform-ref',
                     'not-understood','propagate','propose','proxy','query-if','query-ref','refuse','reject-proposal','request',
                     'request-when','request-whenever','subscribe']




class FIPAMessage(object):
    performative = ''
    sender = ''
    receiver = ''
    reply_to = ''
    content = ''
    language = ''
    encoding = ''
    ontology = ''
    protocol = ''
    conversation_id = ''
    reply_with = ''
    in_reply_to = ''
    reply_by = ''
    message = ''
    
    fname = ''
    fdescription = ''
    fvalues = ''
    
    def set_performative(self, val):
        for t in FIPA_performative:
            if t == val:
                self.performative = val
                self.message = "(" + self.performative + "\n"
                break
            
    def get_performative(self):
        return self.performative
    
    def set_sender(self, val):
        self.sender = val
        self.message = self.message + "\t:sender " + self.sender + "\n"
    def get_sender(self):
        return self.sender
    
    def set_receiver(self, val):
        self.receiver = val
        self.message = self.message + "\t:receiver " + self.receiver + "\n"
    def get_receiver(self):
        return self.receiver
        
    def set_reply_to(self, val):
        self.reply_to = val
        self.message = self.message + "\t:reply-to " + self.reply_to + "\n"
    def get_reply_to(self):
        return self.reply_to
    
    def set_content(self, val):
        self.content = val
        self.message = self.message + "\t:content " + self.content + "\n"
    def get_content(self):
        return self.content
    
    def set_language(self, val):
        self.language = val
        self.message = self.message + "\t:language " + self.language + "\n"
    def get_language(self):
        return self.language
    
    def set_encoding(self, val):
        self.encoding = val
        self.message = self.message + "\t:encoding " + self.encoding + "\n"
    def get_encoding(self):
        return self.encoding
    
    def set_ontology(self, val):
        self.ontology = val
        self.message = self.message + "\t:ontology " + self.ontology + "\n"
    def get_ontology(self):
        return self.ontology
    
    def set_protocol(self, val):
        self.protocol = val
        self.message = self.message + "\t:protocol " + self.protocol + "\n"
    def get_protocol(self):
        return self.protocol
    
    def set_conversation_id(self, val):
        self.conversation_id = val
        self.message = self.message + "\t:conversation-id " + self.conversation_id + "\n"
    def get_conversation_id(self):
        return self.conversation_id
    
    def set_reply_with(self, val):
        self.reply_with = val
        self.message = self.message + "\t:reply-with " + self.reply_with + "\n"
    def get_reply_with(self):
        return self.reply_with
    
    def set_in_reply_to(self, val):
        self.in_reply_to = val
        self.message = self.message + "\t:in-reply-to " + self.in_reply_to + "\n"
    def get_in_reply_to(self):
        return self.in_reply_to
    
    def set_reply_by(self, val):
        self.reply_by = val
        self.message = self.message + "\t:reply-by " + self.reply_by + "\n"
    def get_reply_by(self):
        return self.reply_by
    
    def close_message(self):
        self.message = self.message + "\n)"
    
    def get_message(self):
        return self.message;
    
    def validade_performative(self, line):
        match = re.search("^\(accept-proposal$", line)
        if match:
            self.performative = "accept-proposal"
        match = re.search("^\(agree$", line)
        if match:
            self.performative = "agree"
        match = re.search("^\(cancel$", line)
        if match:
            self.performative = "cancel"
        match = re.search("^\(cfp$", line)
        if match:
            self.performative = "cfp"
        match = re.search("^\(confirm$", line)
        if match:
            self.performative = "confirm"
        match = re.search("^\(disconfirm$", line)
        if match:
            self.performative = "disconfirm"
        match = re.search("^\(failure$", line)
        if match:
            self.performative = "failure"
        match = re.search("^\(inform$", line)
        if match:
            self.performative = "inform"
        match = re.search("^\(inform-if$", line)
        if match:
            self.performative = "inform-if"
        match = re.search("^\(inform-ref$", line)
        if match:
            self.performative = "inform-ref"
        match = re.search("^\(not-understood$", line)
        if match:
            self.performative = "not-understood"
        match = re.search("^\(propagate$", line)
        if match:
            self.performative = "propagate"
        match = re.search("^\(propose$", line)
        if match:
            self.performative = "propose"
        match = re.search("^\(proxy$", line)
        if match:
            self.performative = "proxy"
        match = re.search("^\(query-if$", line)
        if match:
            self.performative = "query-if"
        match = re.search("^\(query-ref$", line)
        if match:
            self.performative = "query-ref"
        match = re.search("^\(refuse$", line)
        if match:
            self.performative = "refuse"
        match = re.search("^\(reject-proposal$", line)
        if match:
            self.performative = "reject-proposal"
        match = re.search("^\(request$", line)
        if match:
            self.performative = "request"
        match = re.search("^\(request-when$", line)
        if match:
            self.performative = "request-when"
        match = re.search("^\(request-whenever$", line)
        if match:
            self.performative = "request-whenever"
        match = re.search("^\(subscribe$", line)
        if match:
            self.performative = "subscribe"
                
        #print("Performative: ", self.performative)
        return self.performative
    
    
    def set_fname(self, val):
        self.fname = val
    def get_fname(self):
        return self.fname
    
    def set_fdescription(self, val):
        self.fdescription = val
    def get_fdescription(self):
        return self.fdescription
    
    def set_fvalues(self, val):
        self.fvalues = val
    def get_fvalues(self):
        return self.fvalues
    
    
    
    def analyze_content(self, content):
        description = ''
        action_function = ''
        values = ''
        #Format:
        #"Description (= (action_function) (Values1)(Values(2)(ValuesN))"
        
        match = re.search("^(\w+)(.*)\(=", content, re.DOTALL|re.MULTILINE)
        if match:
            field = match.group(0).lstrip()
            match2 = re.search("^\w+(.?)(\w+)?",field)
            if match2:
                description = match2.group(0)
                #print("Description: ", description)
  
        match = re.search("\(=(.)\([a-z-]+\)(.)\(.*\)", content, re.DOTALL|re.MULTILINE)
        if match:
            field = match.group(0).lstrip()
            #print("Field: ", field)
            match2 = re.search("\(([a-z0-9-]+)\)",field)
            if match2:
                action_function = match2.group(1).lstrip()
                #print("Action function: ", action_function)
            match4 = re.search(".*\((.*)\)\)",field, re.DOTALL|re.MULTILINE)
            if match4:
                values = match4.group(1)  
                print("Values: ", values)
        
        self.fdescription = description
        self.fname = action_function
        self.fvalues = values
  
  
  
        
    def parse_pkg(self, pkg):
        f = io.StringIO(pkg)
        for line in f:
            match = re.search("^\([a-z0-9\-]+$", line)
            if match:
                self.validade_performative(line)
            match = re.search(":sender(.\w+)", line)
            if match:
                sender = match.group(1).lstrip()
                #print("Sender: ", sender)
                self.sender = sender
            match = re.search(":receiver(.\w+)", line)
            if match:
                receiver = match.group(1).lstrip()
                self.receiver = receiver
                #print("Receiver: ", receiver)
            match = re.search(":reply-with(.\w+)", line)
            if match:
                repwith = match.group(1).lstrip()
                #print("Reply-with: ", repwith)
                self.reply_with = repwith
            match = re.search(":conversation-id(.\w+)", line)
            if match:
                convid = match.group(1).lstrip()
                #print("Convertation-id: ", convid)
                self.conversation_id = convid

        f = io.StringIO(pkg)
        mg = ''        
        z = ''
        for lin in f:
            z += lin
        rx_sequence=re.compile(r":content(.*)\)",re.DOTALL|re.MULTILINE)
        for match in rx_sequence.finditer(z):
            mg = match.group(1)
            self.analyze_content(mg.lstrip())
        
 