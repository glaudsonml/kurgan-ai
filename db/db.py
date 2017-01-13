import sqlite3



class DB(object):
    conn = None
    

    def getData(self, query, database):
        result = []
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            result.append(row) 
        conn.close()
        return result
    
    def setData(self, query, database):
        result = []
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.close()
        
    