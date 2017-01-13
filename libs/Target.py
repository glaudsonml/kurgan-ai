'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@vortexai.com.br>

Created in May, 11th 2016.
'''
import requests
import config
import sys
import warnings
import validators

sys.path.append('../')

class Target(object):
    host = None
    method = ''
    headers = {}
    uri = ''
    webserver = ''
    scheme = ''
    port = ''
    path = ''
    url = ''
    baseUrl = ''
    
    def __init__(self):
        method = 'GET'
        headers = {'User-Agent':'Kurgan-AI/0.0.1'}
        uri = '/'
        scheme = 'http'
    
    
    def set_host(self, val):
        self.host = val
    def get_host(self):
        return self.host
    
    def set_port(self, val):
        self.port = val
    def get_port(self):
        return self.port
    
    def set_method(self, val):
        self.method = val
    def get_method(self):
        return self.method
    
    def set_headers(self,val):
        self.headers = val
    def get_headers(self):
        return self.headers

    def set_webserver(self, val):
        self.webserver = val
    def get_webserver(self):
        return self.webserver

    def set_scheme(self, val):
        self.scheme = val
    def get_scheme(self):
        return self.scheme
    
    def set_path(self,val):
        self.path = val
    def get_path(self):
        return self.path
    
    def set_url(self, val):
        self.url = val
    def get_url(self):
        return self.url
    
    def set_baseUrl(self, val):
        self.baseUrl = val
    def get_baseUrl(self):
        return self.baseUrl
    
        
    def send_request(self):
        warnings.filterwarnings('ignore')
        url = self.scheme+'://'+self.host+':'+str(self.port)+"/"+str(self.path)
        if config.FOLLOW_URL is True:
            r = requests.get(url, allow_redirects=True, verify=False)
        else:
            r = requests.get(url, allow_redirects=False, verify=False)     
        return r

    def send_request_head(self, v_url):
        warnings.filterwarnings('ignore')
        if config.FOLLOW_URL is True:
            r = requests.request('HEAD',v_url, allow_redirects=True, verify=False)
        else:
            r = requests.request('HEAD',v_url, allow_redirects=False, verify=False)     
        return r

    
    
    def get_options(self):
        url = self.scheme+'://'+self.host+':'+str(self.port)+"/"+str(self.path)
        r = requests.options(url)
        if r.status_code == 200:
                if 'allow' in r.headers:
                    return r.headers['allow']
        else:
                return None