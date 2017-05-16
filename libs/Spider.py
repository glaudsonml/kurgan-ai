'''
Spider url.
'''

import requests
import re
import validators
from furl import *
from urllib.parse import urlparse

from libs.Target import Target as T
from html.parser import HTMLParser
import config as cf


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MyHTMLParser(HTMLParser):
    links = []
    rlinks = []
    
    def add_link(self, val):
        self.links.append(val)
        
    def get_links(self):
        for i in self.links:
            if i not in self.rlinks:
                self.rlinks.append(i)
        return self.rlinks
        #return self.links
    
    def zera_links(self):
        for j in  self.links:        
            self.links.remove(j)

    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key,value) in attrs:
                if key == 'href':
                    self.links.append(value)
        if tag == 'script':
            for (key,value) in attrs:
                if key == 'src':
                    self.links.append(value)
        if tag == 'link':
            for (key,value) in attrs:
                if key == 'href':
                    self.links.append(value)
        if tag == 'form':
            for (key,value) in attrs:
                if key == 'action':
                    self.links.append(value)



class Spider(object):
    baseUrl = ''
    dictionary = ''
    response_body = ''
    links = []
    javascripts = []
    origUrl = ''
    getAll = False
        
    def set_baseUrl(self, val):
        self.baseUrl = val
    def get_baseUrl(self):
        return self.baseUrl
    
    def set_origUrl(self, val):
        self.origUrl = val
    def get_origUrl(self):
        return self.origUrl
    
    def set_response_body(self, val):
        self.response_body = val
    def get_response_body(self):
        return self.response_body
    
    def set_links(self, val):
        self.links.append(val)  
    def get_links(self):
        return self.links
#    def zera_links(self):
#        for val in self.links:
#            self.links.remove(val)
        
    def set_getAll(self, val):
        self.getAll = val
    def get_getAll(self):
        return self.getAll

    def send_request(self, url):
        if cf.FOLLOW_URL is True:
            r = requests.get(url, allow_redirects=True, verify=False)
        else:
            r = requests.get(url, allow_redirects=False, verify=False)     
        return r

    def send_request_head(self, v_url):
        warnings.filterwarnings('ignore')
        if cf.FOLLOW_URL is True:
            r = requests.request('HEAD',v_url, allow_redirects=True, verify=False)
        else:
            r = requests.request('HEAD',v_url, allow_redirects=False, verify=False)     
        return r


    def get_linksinDomain(self):
        toremove = []
        for i in self.links:
            if (self.baseUrl not in i) or (self.origUrl not in i):
                if ('http' in i) or ('https' in i):
                    toremove.append(i)
        
        for j in toremove:        
            self.links.remove(j)


    def parseHTML(self, response):
        parser = MyHTMLParser()
        parser.feed(response)
        #parser.zera_links()        
        self.links = parser.get_links()
        if self.getAll is False:
            self.get_linksinDomain()
            
        
    def run(self):
        links = ''
        req = self.send_request(self.baseUrl)
        links = self.parseHTML(req.text)
    
        tempLinks = self.get_links()
        counter = 0
        realLinks = []
        for i in tempLinks:
            if re.match("^https?://", i):
                v_link = i
            else:
                v_link = ''
                #base = self.get_baseUrl()
                base = self.baseUrl.split('/')
                index = len(base) 
                for j in range(0,index-1):
                    if j != index-1:
                        v_link += base[j] + "/"
                v_link += i
                
            #    v_link = base + i
        
                print(v_link)
            if validators.url(v_link) is True:
                vresp = self.send_request_head(v_link)
                if vresp.status_code == 200:
                    print(counter, "--" , v_link," -- ",vresp)
                    realLinks.append(v_link)
                counter = counter + 1
        return realLinks
