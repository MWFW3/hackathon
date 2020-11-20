import sqlite3
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(userid INTEGER PRIMARY KEY AUTOINCREMENT,username VARCHAR(255));""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Competences(compid INTEGER  PRIMARY KEY AUTOINCREMENT,competencename VARCHAR(255));""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Questions(qusestid INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UQ(userid INT PRIMARY KEY, qusestid INT,name VARCHAR(255));""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UC(userid INT PRIMARY KEY,compid INT,name VARCHAR(255));""")

def addUser(username):
    cursor.execute("""INSERT INTO Users(username) VALUES('""" + username + """');""")
    conn.commit()

addUser('sem')
