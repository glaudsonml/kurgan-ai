'''
Vulnerability Scanner Class
'''


class VulnScan(object):
    scanning=True
    
    def set_scanning(self, val):
        self.scanning = val
    def get_scanning(self):
        return self.scanning

