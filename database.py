import sqlite3
import json
competences = ['Математика', 'прога', 'unix', 'физика', 'биология', 'БЖД']

conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(userid INTEGER PRIMARY KEY AUTOINCREMENT,telegramid VARCHAR(255));""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Competences(compid INTEGER  PRIMARY KEY AUTOINCREMENT,competencename VARCHAR(255) UNIQUE);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Questions(questid INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UQ(id INTEGER PRIMARY KEY,userid INTEGER, questid INT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS QC(id INTEGER PRIMARY KEY,questid INTEGER, compid INT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UC(id INTEGER PRIMARY KEY,userid INTEGER,compid INT);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Sessions(id INTEGER PRIMARY KEY AUTOINCREMENT,telegramid INTEGER,session JSON);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Pending(id INTEGER PRIMARY KEY AUTOINCREMENT,telegramida INTEGER,telegramidc INTEGER);""")

# telegramidc - creator telegramida - who answer
def addPending(telegramidc,telegramida):
    cursor.execute("""INSERT INTO Pending(telegramidc,telegramida) VALUES(?,?);""", (telegramidc,telegramida))
    conn.commit()
def getPendingUser(telegramid):
    cursor.execute("""SELECT telegramida FROM Pending WHERE telegramidc = ?;""", (str(telegramid),))
    comp = cursor.fetchall()
    return comp[0][0]


def addUser(telegramid):
    if(getUserId(telegramid) == None):
        cursor.execute("""INSERT INTO Users(telegramid) VALUES(?);""",(telegramid,))
        conn.commit()
def addQuestion(telegramid,question,comps):
    cursor.execute("""INSERT INTO Questions(question) VALUES(?);""",(question,))
    conn.commit()
    addQuestionToUser(telegramid, question)
    for i in comps:
        cursor.execute("""INSERT INTO QC(questid,compid) VALUES(?,?);""", (getQuestId(question),getCompId(i)))
        conn.commit()

def addCompsToUser(telegramid, comps):

    for i in comps:
        #print(i)
        cursor.execute("""INSERT INTO UC(userid,compid) VALUES(?,?);""",(getUserId(telegramid),getCompId(i)))
        conn.commit()


def addQuestionToUser(telegramid, quest):
    cursor.execute("""INSERT INTO UQ(userid,questid) VALUES(?,?);""",(getUserId(telegramid),getQuestId(quest)))
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
    cursor.execute("""SELECT compid FROM UC WHERE userid = ?;""", (str(getUserId(telegramid)),))
    comp = cursor.fetchall()


    req = comp
    res = []
    for i in req:

        res.append(getCompetence(i[0]))
    return res


def getCompId(competencename):
    cursor.execute("""SELECT compid FROM Competences WHERE competencename = '""" + competencename + """';""")
    comp = cursor.fetchall()
    return comp[0][0]

def getQuestId(questname):
    cursor.execute("""SELECT questid FROM Questions WHERE question = ? ;""",((str(questname),)))
    comp = cursor.fetchall()
    #print(questname)
   # print(comp)
    res = comp[0][0]
    return res

def getQuestions(id):

    compent = getUserCompetences(id)
    print(compent)
    cmpids = ()
    for i in compent:
        print(i)
        cmpids = cmpids + tuple(str(getCompId(i)))
    qsts = []

    for i in cmpids:
        #print(i)
        cursor.execute("""SELECT questid FROM QC WHERE compid = ? ;""", i)
        comp = cursor.fetchall()
        #print(comp)
        if comp != []:
            for j in comp:
                qsts.append(j[0])
    qsts = set(qsts)
    res =[]
    print(qsts)
    for i in qsts:
        cursor.execute("""SELECT question FROM Questions WHERE questid = ? ;""", (i,))
        comp2 = cursor.fetchall()
        #comp2 = comp2 + (str(getQuestCreator(i)),)
        #print(comp2[0][0])
        res.append([comp2[0][0],getQuestCreator(i)])
    print(res)
    return res
def getQuestCreator(quest_id):
    cursor.execute("""SELECT userid FROM UQ WHERE questid = ? ;""", ((str(quest_id),)))
    comp = cursor.fetchall()
    userid = comp[0][0]

    cursor.execute("""SELECT telegramid FROM Users WHERE userid = ? ;""", (str(userid,)))
    comp2 = cursor.fetchall()
    res = comp2[0][0]
    return res


    # if getCompetence(cur_id) == '':
    #     cursor.execute("""SELECT questid FROM QC WHERE compid = ?;""",(getCompetence(cur_id)))
    #     comp = cursor.fetchall()
    #     return comp[0][0]


def getMyQuestions(id):

    cursor.execute("""SELECT questid FROM UQ WHERE userid = ? ;""", ((str(getUserId(id)),)))
    comp = cursor.fetchall()
    res = []
    for i in comp:
        print(i[0])
        cursor.execute("""SELECT question FROM Questions WHERE questid = ? ;""", ((str(i[0]),)))
        comp2 = cursor.fetchall()
        res.append(comp2)
    return res



def saveSession(id,session):
    cursor.execute("""UPDATE Sessions SET session = ? WHERE telegramid = ?;""", (session,id))
    conn.commit()
def loadSession(id):
    cursor.execute("""SELECT session FROM Sessions WHERE telegramid = ? ;""", (id,))
    comp = cursor.fetchall()
    if comp != []:

        return json.loads(comp[0][0])
    else: return []
def createSession(id,session):
    if (loadSession(id) == []):
        cursor.execute("""INSERT INTO Sessions(telegramid,session) VALUES(?,?);""", (id,session))
        conn.commit()


#add competences if not exist
for i in competences:
    cursor.execute("""INSERT OR IGNORE INTO Competences(competencename) VALUES('""" + i + """');""")
    conn.commit()





#print(getCompetences()[1][0])
#print(getUserId('sem'))
#addUser("sem")
#addCompsToUser('sem', competences)
