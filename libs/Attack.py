'''
Attack Class
'''

class Attack(object):
    attacking=True
    sqli=False
    csrf=False
    xss=False
    rfi=False
    lfi=False
    bf=False
    
    
    def set_attacking(self, val):
        self.attacking = val
    def get_attacking(self):
        return self.attacking
    
    def set_sqli(self, val):
        self.sqli = val
    def get_sqli(self):
        return self.sqli
    
    def set_csrf(self, val):
        self.csrf = val
    def get_csrf(self):
        return self.csrf
    
    def set_xss(self, val):
        self.xss = val
    def get_xss(self):
        return self.xss
    
    def set_rfi(self, val):
        self.rfi = val
    def get_rfi(self):
        return self.rfi
    
    def set_lfi(self, val):
        self.lfi = val
    def get_lfi(self):
        return self.lfi
    
    def set_bf(self, val):
        self.bf = val
    def get_bf(self):
        return self.bf