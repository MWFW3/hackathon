import json
class User:
    def __init__(self, name):
        self.name=name
        self.Comps=[]
        self.QComps = []
        self.Quest = ''
        self.inChoose=False
        self.waitingForQuestion=False
        self.inChooseAsk = False
        self.curQuest = 0
        self.Answering = False
        self.curQuestioner = ''
    def exportSession(self):
        data ={
        'name':self.name,
        'Comps':self.Comps,
        'QComps':self.QComps,
        'Quest':self.Quest,
         'inChoose' :  self.inChoose,
        'waitingForQuestion': self.waitingForQuestion,
        'inChooseAsk':self.inChooseAsk,
        'curQuest': self.curQuest,
        'Answering': self.Answering,
        'curQuestioner':self.curQuestioner
        }
        return json.dumps(data)
    def importSession(self,session):
        self.name = session['name']
        self.Comps = session['Comps']
        self.QComps = session['QComps']
        self.Quest = session['Quest']
        self.inChoose = session['inChoose']
        self.waitingForQuestion = session['waitingForQuestion']
        self.inChooseAsk = session['inChooseAsk']
        self.curQuest = session['curQuest']
        self.Answering = session['Answering']
        self.curQuestioner = session['curQuestioner']