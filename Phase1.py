'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@vortexai.com.br>

Created in May, 11th 2016.
'''

import validators
import re
import libs.Target as T
import libs.WebServer as ws
from furl import *
from urllib.parse import urlparse

import libs.Crawling as cwl
import config as cf

from libs.STOMP import STOMP_Connector
from libs.FIPA import FIPAMessage
import libs.Tree as Tree
def analyze_webserver(target):
    print("Analyzing Webserver....")
    headers = target.get_headers()
    w = ws.WebServer()
    w.set_banner(target.get_webserver())
    
    w.check_server()
    server = w.get_server()
    if server is None:
        print('Server: Unknown')
    else:
        print('Server: ', server)

    w.check_version()
    version = w.get_version()
    if version is None:
        print('Server Version: Unknown')
    else:
        print('Server Version: ', version)

    w.check_os()  
    os = w.get_os()
    if os is None:
        if 'X-RedHat-Debug' in headers:
            w.set_os('RedHat')
        
    os = w.get_os()
    if os is None:
        print('Server OS: Unknown')
    else:
        print('Server OS: ', os)


    path = str(target.get_path())
    if not path[:-1].endswith('/'):
        f = furl(path)
        fseg = f.path.segments[-1]
        extension = fseg.split(".")[-1]
        app = ws.Application()
        app.set_extension(extension)    

    #Try detect framework
    fr = ws.Framework()
    if 'X-Powered-By' in headers:
        fr.set_X_Powered_By(headers['X-Powered-By'])    
        fr.check_framework()

    framework = fr.get_framework()
    if framework is None:
        if 'Content-Type' in headers and 'text/html' in headers['Content-Type']:
            print('Framework: Static HTML')
        else:    
            print('Framework: Unknown')
    else:
        print('Framework: ', framework)

    #get options
    op = target.get_options()
    if op is not None:
        w.set_options(op)
        opt = w.check_options()
        print("Options: ", opt)

    print("")
    
    print("Crawling like Spider...")
    print("Enviando request...")
    req = target.send_request()
    crawling = cwl.Crawling()
    crawling.set_baseUrl(target.get_url())
    crawling.set_getAll(cf.CRAWLING_GET_ALL_LINKS)
    links = crawling.parseHTML(req.text)
    
    #validate links
    #print("links: ", crawling.get_links())
    tempLinks = crawling.get_links()
    counter = 0
    realLinks = []
    for i in tempLinks:
        if re.match("^https?://", i):
            v_link = i
        else:
            base = target.get_baseUrl()
            v_link = base + i
        
        #print(v_link)
        if validators.url(v_link) is True:
                vresp = target.send_request_head(v_link)
                if vresp.status_code == 200:
                    print(counter, "--" , v_link," -- ",vresp)
                    #send data to agents
                    #fpm = FIPAMessage()
                    #fpm.set_performative("cfp")
                    #fpm.set_sender("Board")
                    #fpm.set_receiver("All Agents")
                    #fpm.set_content("(= Analyze ("+v_link+"))")
                    #fpm.set_reply_with("q13ard")
                    #fpm.close_message()
                    #print(fpm.get_message())
                    realLinks.append(v_link)
                counter = counter + 1
    
    
'''
    print("Generating Tree of URLs target...")
    #remove duplicate urls
    realLinks = list(set(realLinks))
    #rootNode = target.get_baseUrl()
    rootNode = str(target.get_baseUrl())
    

    tree = Tree.Tree()
    tree.add_node(str("{0}".format(rootNode)))  # root node

    
    for r_link in realLinks:
        path = urlparse(r_link).path
        parentNodes = []
        pats = []
        pats = path.split("/")
        ind = len(pats)
        #print("len= "+str(ind)+" | ind-1="+pats[ind-1]+" | ind-2="+pats[ind-2])
        if ind == 2:
            knode = str("{0}".format(pats[ind-1]))
            #tree.add_node(knode)
            tree.add_node(knode,rootNode)
            parentNodes.append(str("{0}".format(rootNode)))
        else:
            knode = str("{0}".format(pats[ind-1]))
            kparent = str("{0}".format(pats[ind-2]))
            if pats[ind-2] not in parentNodes:
                parentNodes.append(pats[ind-2])
                tree.add_node(kparent,rootNode)
            tree.add_node(knode,kparent)
            
    print("Display Tree.....")
    tree.display(str("{0}".format(rootNode)))
    
    print("***** DEPTH-FIRST ITERATION *****")
    for node in tree.traverse(str("{0}".format(rootNode))):
        print(node)
    print("***** BREADTH-FIRST ITERATION *****")
    for node in tree.traverse(str("{0}".format(rootNode)), mode=Tree._BREADTH):
        print(node)
   ''' 