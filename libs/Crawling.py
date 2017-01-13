'''
Running Crawling attack using source code reading and brute force uri.
'''

from libs.Target import Target as T
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    links = []
    def get_links(self):
        return self.links
    
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


class Crawling(object):
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

    def set_getAll(self, val):
        self.getAll = val
    def get_getAll(self):
        return self.getAll

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
        self.links = parser.get_links()
        if self.getAll is False:
            self.get_linksinDomain()
    
        
            