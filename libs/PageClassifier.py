'''
Page Classifier
'''
import requests
import re, sys
import warnings
import signal


from bs4 import BeautifulSoup
from time import sleep
from nltk.tokenize import RegexpTokenizer
from requests.packages.urllib3.exceptions import InsecureRequestWarning

USER_AGENT="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"
ACCEPT="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
ACCEPT_LANGUAGE="en-US,en;q=0.5"
ACCEPT_ENCODING="gzip, deflate, br"


class PageClassifier(object):
    session = ''
    url = ''
    type = ''
    page = ''
    proxies = ''
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT, 'Accept': ACCEPT, 'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING})
        self.session.headers.update({'DNT': 1, 'Upgrade-Insecure-Requests':1})
        #self.proxies = {'http':'127.0.0.1:9090'}
        
    
    def set_url(self, val):
        self.url = val
    def get_url(self):
        return self.url
    
    def set_page(self, val):
        self.page = val
    def get_page(self):
        return self.page
    
    def set_type(self, val):
                self.type = val
    def get_type(self):
        return self.type
    
    def connect(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        r = self.session.get(self.url, verify=False, proxies=self.proxies)
        self.page = r.content.decode()
        return r    
    
    def checkIfStatic(self):
        is_static = 0
        r = self.connect()
        if r.status_code != 200:
            print("Not returning 200")

        soup = BeautifulSoup(self.page, 'html.parser')
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        
        text = ''
        total_line_text = 0
        for line in visible_text.splitlines():
            pattern = "[a-zA-Z-0-9]+"
            match = re.search(pattern,line)
            if match:
                text = text + line.lstrip() + "\n"
                total_line_text = total_line_text + 1
        
        if total_line_text > 30:
            #print("More then 30 lines - total: " + str(total_line_text) + ".\n")
            is_static = is_static + 10
            
        #print(texto)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        for t in tokens:
            pattern = "(Login|Username|Usu.rio|Senha|Password|Esqueci|Email)"    
            match3 = re.search(pattern, str(t), re.IGNORECASE)
            if match3:
                #print("More 10" + match3.group(0).lstrip() +"\n")
                is_static = is_static + 10
        
        if is_static > 100:
            is_static = 100
                                
        return is_static
        
    
    def checkIfForgottenPassword(self):
        is_forgotten_password = 0
        text_input = []

        r = self.connect()
        if r.status_code != 200:
            print("Not returning 200")

        soup = BeautifulSoup(self.page, 'html.parser')
        form_input = soup.find_all("input")
        for f in form_input:
            pattern = "type=\"text\""
            match = re.search(pattern, str(f), re.IGNORECASE)
            if match:
                intext = match.group(0).lstrip()
                if intext not in text_input:
                    #print("More 10: " + match.group(0).lstrip() + "\n")
                    is_forgotten_password = is_forgotten_password + 10
                    text_input.append(intext)
            #else:
                #discount = 20
            pattern = "(Login|Username|Usu.rio|Senha|Password|Email)"    
            match3 = re.search(pattern, str(f), re.IGNORECASE)
            if match3:
                intext = match3.group(0).lstrip()
                if intext not in text_input:
                    #print("More 10" + match3.group(0).lstrip() +"\n")
                    is_forgotten_password = is_forgotten_password + 10
                    text_input.append(intext)

        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        
        text = ''
        total_line_text = 0
        for line in visible_text.splitlines():
            pattern = "[a-zA-Z-0-9]+"
            match = re.search(pattern,line)
            if match:
                text = text + line.lstrip() + "\n"
                total_line_text = total_line_text + 1
        
        if total_line_text < 10:
            #print("More 10 - Few line text, only " + str(total_line_text) + ".\n")
            is_forgotten_password = is_forgotten_password + 10
            
        #print(texto)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        for t in tokens:
            pattern = "(Login|Username|Usu.rio|Esqueci|Email|Recover|Forgotten|Recuperar)"    
            match3 = re.search(pattern, str(t), re.IGNORECASE)
            if match3:
                #print("More 10" + match3.group(0).lstrip() +"\n")
                is_forgotten_password = is_forgotten_password + 10
        
        if is_forgotten_password > 100:
            is_forgotten_password = 100
                                
        return is_forgotten_password


    def checkIfAuthForm(self):
        is_authform = 0
        text_input = []
        r = self.connect()
        if r.status_code != 200:
            print("Not returning 200")

        soup = BeautifulSoup(self.page, 'html.parser')
        form_input = soup.find_all("input")
        for f in form_input:
            pattern = "type=\"password\""
            match = re.search(pattern, str(f), re.IGNORECASE)
            if match:
                intext = match.group(0).lstrip()
                if intext not in text_input:
                    print("More 40: " + match.group(0).lstrip() + "\n")
                    is_authform = is_authform + 40
                    text_input.append(intext)
            #else:
                #discount = 20
                
            pattern = "type=\"text\""
            match2 = re.search(pattern, str(f), re.IGNORECASE)
            if match2:
                pattern = "(Login|Username|Usu.rio|Senha|Password)"    
                match3 = re.search(pattern, str(f), re.IGNORECASE)
                if match3:
                    intext = match3.group(0).lstrip()
                    if intext not in text_input:
                        print("More 10" + match3.group(0).lstrip() +"\n")
                        is_authform = is_authform + 10
                        text_input.append(intext)
        
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        
        text = ''
        total_line_text = 0
        for line in visible_text.splitlines():
            pattern = "[a-zA-Z-0-9]+"
            match = re.search(pattern,line)
            if match:
                text = text + line.lstrip() + "\n"
                total_line_text = total_line_text + 1
        
        if total_line_text < 10:
            #print("More 10 - Few line text, only " + str(total_line_text) + ".\n")
            is_authform = is_authform + 10
            
        #print(texto)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        for t in tokens:
            pattern = "(Login|Username|Usu.rio|Senha|Password|Esqueci|Email)"    
            match3 = re.search(pattern, str(t), re.IGNORECASE)
            if match3:
                intext = match3.group(0).lstrip()
                if intext not in text_input:
                    #print("More 10" + match3.group(0).lstrip() +"\n")
                    is_authform = is_authform + 10
                    text_input.append(intext)
                    
        if is_authform > 100:
            is_authform = 100
                                
        return is_authform
        


def handler(signum, frame):
    print("\n\nStop execution...\n", signum);
    sys.exit(0)
    

def Analyze(url):
    print("Trying Classify url: " + url)
    pc = PageClassifier()
    pc.set_url(url)
    
    is_authform = pc.checkIfAuthForm()
    print("Is Authentication Form Page: {0:.0f}%".format(is_authform))
    
    is_static = pc.checkIfStatic()
    print("Is Static HTML Page: {0:.0f}%".format(is_static))

    is_forgotten_password = pc.checkIfForgottenPassword()
    print("Is Forgotten Password Page: {0:.0f}%".format(is_forgotten_password))

    
def show_help():
    print("Kurgan AI - Framework  WEB Security Analyzer")
    print("http://www.kurgan.com.br/")
    print("Page Classifier")
    print("Usage: python3 " + __file__ + " <url>")
    
    

def main(args):
    signal.signal(signal.SIGINT, handler)
    if args is None:
        show_help()
    else:
        url = args[0]
        Analyze(url)
        
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_help()
    else:
        main(sys.argv[1:]) 
    
