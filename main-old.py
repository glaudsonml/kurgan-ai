'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@vortex-ai.com.br>

Created in May, 11th 2016.
'''

import sys
import libs.Target as T
import Phase1 as p1
import Phase2 as p2
from furl import *
import config as cf

#from urllib.parse import urlparse

def run_phase_1(target):
    if cf.PHASE1 is False:
        return
    else:
        print("Running Phase One - Gathering Informations...")
        #print("Servidor WEB:", target.get_webserver())
        #print("Headers: ", target.get_headers())
        print("-x-x-x-x-x-x-x-x-x")
        p1.analyze_webserver(target)
        print("-x-x-x-x-x-x-x-x-x")


def run_phase_2(target):
    if cf.PHASE2 is False:
        return
    else:
        print("Running Phase Two - Searching for Vulnerabilities...")
        p2.searchVuln(target)
        print("-x-x-x-x-x-x-x-x-x")

def show_help():
    print("Kurgan-Framework version ", cf.VERSION)
    print("Usage: python3 kurgan.py URL")
    print("\nExample:\n")
    print("python3 kurgan.py http://www.vortex-ai.com.br/")
    exit(0)
        
def main(args):
    if args is None:
        show_help()
    else:
        url = args[0]
        o = furl(url)
        #o = urlparse(url)
        scheme = o.scheme
        site = o.host
        if o.port is None:
             port = 80
        else :
            port = o.port
        path = o.path
        
    c = T.Target()    
    c.set_scheme(scheme)
    c.set_host(site)
    c.set_port(port)
    c.set_path(path)
    c.set_url(url)
    if port == 80:
        baseUrl = scheme + "://" + o.host + "/"
    else:
        baseUrl = scheme + "://" + o.host + ":" + str(port) + "/"
    c.set_baseUrl(baseUrl)
    
    mtarget = c.get_host()
    mport = c.get_port()

    #First checking is host is alive!
    if (mtarget is None) or (mport < 1 or mport > 65535):
        print("Invalid Target!")
        exit(2)
    else:    
        print("Target: ", mtarget,":",mport)
        r = c.send_request()
        #if r.status_code == auth -> attack using brute force
        if(r.status_code == 200):
            if 'server' in r.headers:
                c.set_webserver(r.headers['Server'])
            else:
                print("Sorry. No Server Banner!")
            c.set_headers(r.headers)
            if cf.PHASE1 is True:
                run_phase_1(c)
            if cf.PHASE2 is True:
                run_phase_2(c)
        else:
            print("HTTP Response: ",r)
            print("Stopping analysis.")
            exit(2)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_help()
    else:
        main(sys.argv[1:])
    