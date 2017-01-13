'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@kurgan.com.br>

Database SQLite Schema.

Created in May, 13th 2016.
'''

import sqlite3

conn = sqlite3.connect('tests.db')
cursor = conn.cursor()

print("Creating table tests...")

cursor.execute("""
CREATE TABLE tests (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        vulndb_id INTEGER NOT NULL, 
        name VARCHAR(128) NOT NULL,
        description TEXT NOT NULL,
        request TEXT NOT NULL,
        response TEXT NOT NULL
);
""")


print('Table created with success.')