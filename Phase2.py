'''
Running Phase 2 - Check for Vulnerabilities.
'''

from libs.Target import Target as T
from libs.WebServer import WebServer as ws
from furl import *

import config as cf
import libs.VulnScan as vs
import libs.Attack as at

import tests.sqli as sqli

def searchVuln(T):
    print("Searching for vulnerabilities using:")
    vscan = vs.VulnScan()
    vscanOn = vscan.get_scanning()
    if vscanOn is True:
        print("\tVulnscan.")
    
    attack = at.Attack()
    attackOn = attack.get_attacking()
    if attackOn is True:
        print("\tAttacks.")
        #attack.set_sqli(True) #read from config
    
    sql_injection = attack.get_sqli()
    if sql_injection is True:
        si = sqli.SqlInjection()
        si.set_url("http://192.168.2.121/news.php?id=1")
        si.run_attack()