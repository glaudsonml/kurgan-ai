'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@kurgan.com.br>

Database SQLite Schema.

Created in May, 13th 2016.
'''

import sqlite3

conn = sqlite3.connect('vulndb.db')
cursor = conn.cursor()

print("Creating table vulnerability...")

cursor.execute("""
CREATE TABLE vulnerability (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        server_id INTEGER NOT NULL, 
        name VARCHAR(128) NOT NULL,
        description TEXT NOT NULL
);
""")


print('Table created with success.')