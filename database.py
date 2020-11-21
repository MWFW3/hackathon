import sqlite3
competences = ['Математика', 'прога', 'unix', 'физика', 'биология', 'БЖД']

conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(userid INTEGER PRIMARY KEY AUTOINCREMENT,telegramid VARCHAR(255));""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Competences(compid INTEGER  PRIMARY KEY AUTOINCREMENT,competencename VARCHAR(255) UNIQUE);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Questions(qusestid INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UQ(id INTEGER PRIMARY KEY,userid INTEGER, qusestid INT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS QC(id INTEGER PRIMARY KEY,questid INTEGER, compid INT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UC(id INTEGER PRIMARY KEY,userid INTEGER,compid INT);""")

def addUser(telegramid):
    if(getUserId(telegramid) == None):
        cursor.execute("""INSERT INTO Users(telegramid) VALUES(?);""",(telegramid,))
        conn.commit()
def addQuestion(question,comps):
    cursor.execute("""INSERT INTO Questions(question) VALUES(?);""",(question,))
    conn.commit()
    for i in comps:
        cursor.execute("""INSERT INTO QC(questid,compid) VALUES(?,?);""", (getQuestId(question),getCompId(i)))
        conn.commit()

def addCompsToUser(telegramid, comps):
    for i in comps:
        cursor.execute("""INSERT INTO UC(userid,compid) VALUES(""" + str(getUserId(telegramid)) + """,""" + str(getCompId(i)) + """);""")
        conn.commit()


def addQuestionToUser(telegramid, quest):
    cursor.execute("""INSERT INTO UC(userid,compid) VALUES(""" + str(getUserId(telegramid)) + """,""" + str(getQuestId(quest)) + """);""")
    conn.commit()


def getCompetences():
    cursor.execute("""SELECT competencename FROM Competences;""")
    comp = cursor.fetchall()
    return comp

def getUserId(telegramid):
    cursor.execute("""SELECT userid FROM Users WHERE telegramid = ?;""",(str(telegramid),))
    comp = cursor.fetchall()
    try:
       res = comp[0][0]
       return res
    except IndexError:
        return None


def getCompetence(id):
    cursor.execute("""SELECT competencename FROM Competences WHERE compid = ?;""", (str(id),))
    comp = cursor.fetchall()
    res = comp[0][0]
    return res


def getUserCompetences(telegramid):
    cursor.execute("""SELECT compid FROM UC WHERE telegramid = ?;""", (str(telegramid),))
    comp = cursor.fetchall()

    req = comp[0]
    res = []
    for i in req:
        res.append(getCompetence(i))
    return res


def getCompId(competencename):
    cursor.execute("""SELECT compid FROM Competences WHERE competencename = '""" + competencename + """';""")
    comp = cursor.fetchall()
    return comp[0][0]

def getQuestId(questname):
    cursor.execute("""SELECT questid FROM Questions WHERE question = '""" + questname + """';""")
    comp = cursor.fetchall()
    return comp[0][0]

def getQuestions(cur_id):
    cursor.execute("""SELECT questid FROM QC WHERE compid = ;""",())
    comp = cursor.fetchall()
    return comp[0][0]


#add competences if not exist
for i in competences:
    cursor.execute("""INSERT OR IGNORE INTO Competences(competencename) VALUES('""" + i + """');""")
    conn.commit()

#print(getCompetences()[1][0])
#print(getUserId('sem'))
#addUser("sem")
#addCompsToUser('sem', competences)
