'''
Running SQL Injection Attack.
'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import pexpect
import re

import shutil



COMMAND="/usr/bin/python ./tools/sqlmap/sqlmap.py"

#TODO: MSG detect WAF
MSG0="(.)all tested parameters appear to be not injectable(.)"
MSG1="(.){1}\[Y/n\](.)"
MSG2="(.){1}\[y/N\](.)"


MSGVULN="(.)is vulnerable(.)"

class SqlInjection(object):
    url = '';
    
    def set_url(self, val):
        self.url = val
    def get_url(self):
        return self.url

    def run_attack(self):
        print("Trying Sql Injection Attack...")
        #shutil.rmtree('//sqlmap/', ignore_errors=True)
        
        target = COMMAND + " -u " + self.url + " -v 0"
        p = pexpect.spawn(target)
        i = p.expect([MSG0, MSG1])
        #print("i=",i)
        if i == 0:
            print("Not Vulnerable.")
            #print(p.readline())
            print("Finished.")
            p.kill(0)
            sys.exit(0)
            
        if i == 1:
            p.send("Y\r")
            k = p.expect([MSG1,MSG2])
            #print("k=",k)
            if k == 0:
                p.send("Y\r")
            else:
                p.send("N\r")
                
            j = p.expect([MSGVULN,"Something"])
            if j == 0:
                print("Vulnerable!!!")
                p.send("N\r")
                #print(p.readline())
                print(p.read())
                print("Finished.")
                p.kill(0)
                p.close()
                sys.exit(0)
        
        p.kill(0)
        p.close()
    