#!/usr/bin/env python3
'''
Kurgan MultiAgent Framework 
http://www.kurgan.com.br/

Kurgan MultiAgent Framework 

Agent to execute phase 1 of penentration test - Reconnaissance

Author: Glaudson Ocampos - <glaudson@kurgan.com.br>
Created in August 09th, 2016.
'''

import sys
from selenium import webdriver
import time

import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
import config as cf


url = "XXX"
driver = webdriver.PhantomJS(executable_path=cf.PHANTOMJS)
driver.get(url)

print(driver.page_source)
driver.close()