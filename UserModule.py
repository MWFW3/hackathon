class User:
    def __init__(self, name):
        self.name=name
        self.Comps=[]
        self.QComps = []
        self.Quest = ''
        self.inChoose=False
        self.waitingForQuestion=False
        self.inChooseAsk = False
        self.curQuest = 1