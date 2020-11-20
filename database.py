import sqlite3
competences = ['Математика', 'прога', 'unix', 'физика', 'биология', 'БЖД']

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(userid INTEGER PRIMARY KEY AUTOINCREMENT,username VARCHAR(255));""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Competences(compid INTEGER  PRIMARY KEY AUTOINCREMENT,competencename VARCHAR(255) UNIQUE);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Questions(qusestid INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UQ(id INTEGER PRIMARY KEY,userid INTEGER, qusestid INT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UC(id INTEGER PRIMARY KEY,userid INTEGER,compid INT);""")

def addUser(username):
    cursor.execute("""INSERT INTO Users(username) VALUES('""" + username + """');""")
    conn.commit()
def addQuestion(question):
    cursor.execute("""INSERT INTO Questions(question,questioneer) VALUES('""" + question + """');""")
    conn.commit()

def addCompsToUser(username, comps):
    for i in comps:
        cursor.execute("""INSERT INTO UC(userid,compid) VALUES(""" + str(getUserId(username)) + """,""" + str(getCompId(i)) + """);""")
        conn.commit()


def addQuestionToUser(username, quest):
    cursor.execute("""INSERT INTO UC(userid,compid) VALUES(""" + str(getUserId(username)) + """,""" + str(getQuestId(quest)) + """);""")
    conn.commit()


def getCompetences():
    cursor.execute("""SELECT competencename FROM Competences;""")
    comp = cursor.fetchall()
    return comp

def getUserId(username):
    cursor.execute("""SELECT userid FROM Users WHERE username = '""" + username + """';""")
    comp = cursor.fetchall()
    return comp[0][0]


def getCompId(competencename):
    cursor.execute("""SELECT compid FROM Competences WHERE competencename = '""" + competencename + """';""")
    comp = cursor.fetchall()
    return comp[0][0]

def getQuestId(questname):
    cursor.execute("""SELECT questid FROM Questions WHERE question = '""" + questname + """';""")
    comp = cursor.fetchall()
    return comp[0][0]




#add competences if not exist
for i in competences:
    cursor.execute("""INSERT OR IGNORE INTO Competences(competencename) VALUES('""" + i + """');""")
    conn.commit()

#print(getCompetences()[1][0])
#print(getUserId('sem'))
addUser('sem')
addCompsToUser('sem', competences)