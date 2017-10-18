#!/usr/bin/python3
#Kurgan AI - Artificial Intelligence Security Analyzer Framework
#http://www.kurgan.com.br/
#
#Glaudson Ocampos - <glaudson@kurgan.com.br>
#

import os, sys
import re
import sys
import signal
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

current_dir = os.path.basename(os.getcwd())
if current_dir == "agents":
    sys.path.append('../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')

import config as cf

class PageFormClassifier(object):
    data = ''
    isAuthForm = False
    accuracy = 0
    driver = ''
    url = ''
    page = ''
    type = ''

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
    
    def set_data(self, val):
        self.data = val
    def get_data(self):
        return self.data

    
    def get_isAuthform(self):
        return self.isAuthForm
    
    def get_Accuracy(self):
        return self.accuracy 
    
    
    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.binary_location = cf.CHROME_HEADLESS
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.wait = WebDriverWait(self.driver, 5)
        return self.driver
     
    
    def get_page(self):
        self.driver = self.init_driver()
        self.driver.get(self.url)
        self.driver.implicitly_wait(4)
        #target = driver.find_element_by_tag_name('body')
        target = self.driver.find_element_by_tag_name('form')
        visible_text = target.text
        
        for line in visible_text.splitlines():
            pattern = "[a-zA-Z-0-9]+"
            match = re.search(pattern,line)
            if match:
                self.data += line.lstrip() + "\n"

        self.driver.quit()

    
    
    
    def run(self):
        train = [
                 ('Login:', 'form_login'),
                 ('Password:', 'form_login'),
                 ('Forget Your Password.', 'form_login'),
                 ('Type your email.', 'form_login'),
                 ("Type your login", 'form_login'),
                 ('Email or Phone', 'form_login'),
                 ('Forgot Email?.', 'form_login'),
                 ('Sign In', 'form_login'),
                 ("Entrar", 'form_login'),
                 ('Email,telefone ou skype', 'form_login'),
                 ('Usuario', 'form_login'),
                 ('Senha', 'form_login'),
                 ('usuario@dominio', 'form_login'),
                 ('Acessar', 'form_login'),
                 ('Search', 'not_form_login'),
                 ('Pesquisar', 'not_form_login'),
                 ('Procurar', 'not_form_login'),
                 ('Noticias', 'not_form_login'),
                 ('News', 'not_form_login'),
                 ('Buscar', 'not_form_login'),
                 ('Busque', 'not_form_login'),
                 ('Logout', 'not_form_login'),
                 ('Sair', 'not_form_login'),
                 ('Desconectar', 'not_form_login')
                 ]
        test = [
                ('Sign In to continue', 'form_login'),
                ('Criar minha conta', 'form_login'),
                ('Busque na WEB', 'not_form_login'),
                ('Aperte para desconectar', 'not_form_login')
                ]

        cl = NaiveBayesClassifier(train)

        blob = TextBlob(self.data, classifier=cl)
        classified = ''

        for sentence in blob.sentences:
            print("Sentence: \n\n" + str(sentence))
            print("Form Classified as: " + sentence.classify())
            classified = sentence.classify()
        
        if classified is 'form_login':
            self.isAuthForm = True
        else:
            self.isAuthForm = False
            
        print("Accuracy: {0}".format(cl.accuracy(test)))
        self.accuracy = '{0}'.format(cl.accuracy(test))
        return
        

def handler(signum, frame):
    print("\n\nStop execution...\n", signum);
    sys.exit(0)
    

def Analyze(url):
    print("Trying Classify url: " + url)
    pc = PageFormClassifier()
    pc.set_url(url)
    pc.get_page()
    pc.run()
    
    is_authform = pc.get_isAuthform()
    if is_authform is True:
        print("It is Authentication Form Page: " +  '{:.0%}'.format(float(pc.get_Accuracy())))
    else:
        print("It is not Authentication Form Page: " + '{:.0%}'.format(float(pc.get_Accuracy())))

    
def show_help():
    print("Kurgan AI - Framework  WEB Security Analyzer")
    print("http://www.kurgan.com.br/")
    print("Page Form Classifier Using NLP.")
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
    
