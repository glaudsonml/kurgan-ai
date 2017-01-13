'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@vortexai.com.br>

Created in May, 16th 2016.
'''

from requests import *

class Http_Packet():
    schema = ''
    method = {'GET','POST','HEAD','TRACE','OPTIONS','PUT'}
    headers = ''
    

def send_options():
    verbs = requests.options('http://a-good-website.com/api/cats')
    print(verbs.headers['allow'])

def send_request(): 