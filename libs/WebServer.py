'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@vortexai.com.br>

Created in May, 11th 2016.
'''

import db.db as db
import config as cf

class WebServer(object):
    banner = None
    os = None
    server = None
    framework = None
    version = None
    options = None
    
    def set_banner(self, val):
        self.banner = val
    def get_banner(self):
        return self.banner
    
    def set_os(self, val):
        self.os = val
    def get_os(self):
        return self.os
    
    def set_server(self, val):
        self.server = val
    def get_server(self):
        return self.server
    
    def set_version(self,val):
        self.version = val
    def get_version(self):
        return self.version
    
    def set_options(self,val):
        self.options = val
    def get_options(self):
        return self.options
        
    def check_os(self):
        os_possibles = {"Debian","Fedora","Windows","SuSE","marrakesh","RedHat","Unix"}
        for i in os_possibles:
            if i in self.banner:
                self.os = i
                break
    
    
    def check_server(self):
        #server_possibles = {"nginx", "Apache", "Tomcat", "JBoss", "IIS", "X-Varnish"}
        mydb = db.DB();
        query = "SELECT DISTINCT name FROM server"
        database = cf.DB_WEBSERVERS
        servers_in_database = mydb.getData(query,database)
        server_possibles = list(servers_in_database)
        for j in server_possibles:
            for i in j:
                if i in self.banner:
                    self.server = i
                    break
        
    def check_version(self):
        if self.server is None:
            return None
        
        else:
            mydb = db.DB();
            name = self.server;
            query = "SELECT DISTINCT version FROM server WHERE name='" + name + "'"
            database = cf.DB_WEBSERVERS
            servers_in_database = mydb.getData(query,database)
            v_possibles = list(servers_in_database)
            for j in v_possibles:
                for i in j:
                    if i in self.banner:
                        self.version = i
                        break

        
    def check_options(self):
        op_possibles = {'GET','POST','PUT','HEAD','OPTIONS','DELETE','TRACE','PATCH','CONNECT'}
        op_in_server = []
        for i in op_possibles:
            if i in self.options:
                op_in_server.append(i)
        return op_in_server


class Framework(object):
    framework = None
    X_Powered_By = None
    
    def set_X_Powered_By(self, val):
        self.X_Powered_By = val
    def get_X_Powered_By(self):
        return self.X_Powered_By
    
    def set_framework(self, val):
        self.framework = val
    def get_framework(self):
        return self.framework

    #checar extensao tambem
    def check_framework(self):
        fw_possibles = {"PHP","ASP.NET","JSP","Perl","CGI"}
        for i in fw_possibles:
            if i in self.X_Powered_By:
                self.framework = i
                break


class Application(object):
    extension = None
    cookie = None
    has_javascript = None
    
    def set_extension(self, val):
        self.extension = val
    def get_extension(self):
        return self.extension
    
    def set_cookie(self, val):
        self.cookie = val
    def get_cookie(self):
        return self.cookie
    
    def set_has_javascript(self, val):
        self.has_javascript = val
    def get_has_javascript(self):
        return self.has_javascript

    def check_extension(self):
        if self.extension is 'html':
            weight_html_framework += 10
        
    