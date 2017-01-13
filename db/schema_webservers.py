'''
Kurgan AI Web Application Security Analyzer.
http://www.kurgan.com.br/

Author: Glaudson Ocampos - <glaudson@kurgan.com.br>

Database SQLite Schema.

Created in May, 13th 2016.
'''
import sqlite3

conn = sqlite3.connect('webservers.db')
cursor = conn.cursor()

print("Creating table server...")

cursor.execute("""
CREATE TABLE server (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        version VARCHAR(65)
);
""")

#List of WebServers and Versions
 
ws = [(1,"Apache","2.0"),
        (2,"Apache","2.2"),
        (3,"Apache","4.0"),
        (4,"nginx","1.8"),
        (5,"nginx","1.9"),
        (6,"nginx","1.10"),
        (7,"jetty","9.0"),
        (8,"jetty","9.1"),
        (9,"jetty","9.2"),
        (10,"jetty","9.3"),
        (11,"iis","7.0"),
        (12,"iis","7.5"),
        (13,"iis","8.0"),
        (14,"iis","8.5"),
        (15,"iis","10.0"),
        (16,"nginx","1.11.1"),
        (17,"Apache","2.4.10"),
        (18,"Microsoft-IIS","8.0"),
        (19,"Microsoft-IIS","8.5"),
        (20,"Microsoft-IIS","7.5"),
        ]

for data in ws:
    cursor.execute("INSERT INTO server VALUES(?,?,?)",data);



print('Table created with success.')

print("Creating table application...")
cursor.execute("""
CREATE TABLE application (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        version VARCHAR(65)
);
""")

print('Table created with success.')

print("Creating table framework...")
cursor.execute("""
CREATE TABLE framework (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        version VARCHAR(65)
);
""")



conn.close()