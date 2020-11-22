import telebot
import emoji
from UserModule import User
import database as db
bot = telebot.TeleBot('1408437105:AAERPrZPLbkGoHN9HzObvYScyGBQNbwZzoY')

#dictUser={}
comps = db.competences

@bot.message_handler(commands=['start'])
def start(message):
    user = User(message.chat.username)
    #dictUser[message.chat.id] = user

    db.addUser(str(message.chat.id))

    db.createSession(message.chat.id,user.exportSession())

    #print(db.loadSession(message.chat.id))



    # user=User(message.chat.username)
    # dictUser[message.chat.id]=user



    msg="Приветствую тебя студент, здесь ты можешь задавать вопросы другим студентам или отвечать сам на то, в чём разбираешься."
    msg+="Нажми \"добавить компетенцию\", чтобы указать, чем владеешь или сразу задай вопрос"
    bot.send_message(message.chat.id, msg, reply_markup=drawMainMenu())


    #print(user.exportSession())

#----------------------------------------------------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Добавить компетенцию")
def addComp(message):

    dictUser = loadSession(message.chat.id)
    dictUser.inChoose=True

    msg="Выбирайте:"
    markup = telebot.types.ReplyKeyboardMarkup()
    for i in comps:
        markup.add(telebot.types.KeyboardButton(i))
    markup.add(telebot.types.KeyboardButton("ВСЁ ВЫБРАЛ"))
    bot.send_message(message.chat.id, msg, reply_markup=markup)
    db.saveSession(message.chat.id,dictUser.exportSession())
    print(dictUser.name)
    print(dictUser.inChoose)

@bot.message_handler(func=lambda message: message.text == "ВСЁ ВЫБРАЛ")
def finishChoose(message):
    dictUser = loadSession(message.chat.id)

    if dictUser.inChoose:
        dictUser.inChoose=False
        msg="Спасибо, вы выбрали компетенции"

        db.addCompsToUser(message.chat.id, dictUser.Comps)
        dictUser.Comps = []
        db.saveSession(message.chat.id, dictUser.exportSession())
    else:
        msg="Вы ещё не выбрали свои компетенции"
    bot.send_message(message.chat.id, msg, reply_markup=drawMainMenu())
    print(dictUser.name)

#----------------------------------------------------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Задать вопрос")
def ask(message):
    dictUser = loadSession(message.chat.id)

    dictUser.waitingForQuestion=True
    dictUser.inChooseAsk = True
    msg="Выберите компетенции вашего вопроса"
    markup = telebot.types.ReplyKeyboardMarkup()
    for i in comps:
        markup.add(telebot.types.KeyboardButton(i))
    markup.add(telebot.types.KeyboardButton("Готово"))
    bot.send_message(message.chat.id, msg, reply_markup=markup)
    #db.addQuestion(message.chat.id,message.text,comps)

    db.saveSession(message.chat.id, dictUser.exportSession())
@bot.message_handler(func=lambda message: message.text == "Готово")
def submitAskComp(message):
    dictUser = loadSession(message.chat.id)

    if dictUser.inChooseAsk:
        dictUser.inChooseAsk=False

        msg="Теперь напишите текст вашего вопроса"
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.add('Отменить отправку вопроса')
        markup.add('Отправить')

        bot.send_message(message.chat.id, msg, reply_markup=markup)
        #db.addCompsToUser(message.chat.username, dictUser[message.chat.id])
        db.saveSession(message.chat.id, dictUser.exportSession())
    else:
        bot.send_message(message.chat.id, "Вы ещё не выбрали компетенции, относящиеся к вашему вопросу", reply_markup=drawMainMenu())
    print(dictUser.name)
@bot.message_handler(func=lambda message: message.text == "Отправить")
def submitAsk(message):
    dictUser = loadSession(message.chat.id)

    if dictUser.waitingForQuestion:
        dictUser.waitingForQuestion=False
        msg = "Вопрос отправлен!"
        db.addQuestion(message.chat.id, dictUser.Quest, dictUser.QComps)
        dictUser.QComps = []
        print(dictUser.name)
        db.saveSession(message.chat.id, dictUser.exportSession())
    else:
        msg="Вы ещё не задали вопрос и не можете его отправить"
    bot.send_message(message.chat.id, msg, reply_markup=drawMainMenu())

#-------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Ответить на вопрос")
@bot.message_handler(func=lambda message: message.text == "Следующий")
def askQuestions(message):
    dictUser = loadSession(message.chat.id)


    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add("Следующий")
    markup.add("Ответить")
    markup.add("Предложить обменяться контактами + сообщение")
    markup.add("Хватит")

    msg = db.getQuestions(message.chat.id)
    if len(msg)!=0:
        print("автор: " + str(msg[0][1]))
        print(msg)
        print("вопросы: " + str(msg))
        try:
            msgt = msg[dictUser.curQuest][0]
        except IndexError:
            dictUser.curQuest = 0
        msgt = msg[dictUser.curQuest][0]
        dictUser.curQuestioner = msg[dictUser.curQuest][1]
        bot.send_message(message.chat.id, msgt, reply_markup=markup)

        dictUser.curQuest += 1
        print(dictUser.name)
    else:
        bot.send_message(message.chat.id, "Нет актуальных вопросов", reply_markup=drawMainMenu())
    db.saveSession(message.chat.id, dictUser.exportSession())
#-------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Предложить обменяться контактами + сообщение")
def answerwithcontacts(message):
    dictUser = loadSession(message.chat.id)
    markup = telebot.types.ReplyKeyboardMarkup()
    dictUser.Answering = True
    markup.add("Отправить сообщение и запросить контакт")
    db.addPending(dictUser.curQuestioner,message.chat.id)
    bot.send_message(message.chat.id, 'Напишите ответ пользователю', reply_markup=markup)
    db.saveSession(message.chat.id, dictUser.exportSession())
# -------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Отправить сообщение и запросить контакт")
def answer(message):
    dictUser = loadSession(message.chat.id)

    markp = telebot.types.ReplyKeyboardMarkup()
    markp.add("Поделиться контактами")
    markp.add("Не делиться контактами")
    bot.send_message(dictUser.curQuestioner,"Хэй, кто-то ответил на твой вопрос и запросил твои контакты: " + dictUser.Quest, reply_markup=markp)
    dictUser.Answering = False
    dictUser.Quest = ''
    bot.send_message(message.chat.id, 'Ответ и запрос отправлен', reply_markup=drawMainMenu())
    db.saveSession(message.chat.id, dictUser.exportSession())
# -------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Поделиться контактами")
def answer(message):
    markp = telebot.types.ReplyKeyboardMarkup()
    pend = db.getPendingUser(message.chat.id)
    bot.send_message(pend, "Приятной учебы! Запрос на персональную коммуникацию принят лови ссылку: ["+ message.chat.username +"](tg://user?id="  + str(message.chat.id) + ")" , reply_markup=markp, parse_mode='Markdown')
    bot.send_message(message.chat.id,"Удачной учебы! Телеграмм: ["+ bot.get_chat(pend).username +"](tg://user?id="  + str(pend) + ")", reply_markup=markp, parse_mode='Markdown')

#-------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Ответить")
def answer(message):
    dictUser = loadSession(message.chat.id)
    markup = telebot.types.ReplyKeyboardMarkup()
    dictUser.Answering = True
    markup.add("Отправить сообщение")
    bot.send_message(message.chat.id, 'Напишите ответ пользователю', reply_markup=markup)
    db.saveSession(message.chat.id, dictUser.exportSession())


# -------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Отправить сообщение")
def answer(message):
    dictUser = loadSession(message.chat.id)

    markp = telebot.types.ReplyKeyboardMarkup()
    markp.add("Вопрос решен")
    markp.add("Вопрос не решен")
    bot.send_message(dictUser.curQuestioner,"Хэй, кто-то ответил на твой вопрос: " + dictUser.Quest, reply_markup=markp)
    dictUser.Answering = False
    dictUser.Quest = ''
    bot.send_message(message.chat.id, 'Ответ отправлен', reply_markup=drawMainMenu())
    db.saveSession(message.chat.id, dictUser.exportSession())


#-------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "Мои вопросы")
def myQuestions(message):


    msg = db.getMyQuestions(message.chat.id)
    for i in msg:
        bot.send_message(message.chat.id, i, reply_markup=drawMainMenu())

    #print(dictUser[message.chat.id].name)

#-------------------------------------------------------------


@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, "reseted", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text == "Хватит")
def mainMenu(message):
    bot.send_message(message.chat.id, "Давай передохнём от этих вопросов", reply_markup=drawMainMenu())



@bot.message_handler(func=lambda message: message.text !=" ")
def hadlerOfAny(message):
    dictUser = loadSession(message.chat.id)
    msg="-"
    if dictUser.inChoose:
        for i in comps:
            if i==message.text:
                dictUser.Comps.append(i)
                break
        print(dictUser.name)
        print(dictUser.Comps)
    if dictUser.inChooseAsk:
        for i in comps:
            if i==message.text:
                dictUser.QComps.append(i)
                break
        print(dictUser.name)
        print(dictUser.QComps)
    if dictUser.waitingForQuestion:
        dictUser.Quest=message.text
        print(dictUser.Quest)
    if dictUser.Answering:
        dictUser.Quest = message.text
    db.saveSession(message.chat.id, dictUser.exportSession())
def drawMainMenu():
    markup = telebot.types.ReplyKeyboardMarkup()
    addSkill = telebot.types.KeyboardButton("Добавить компетенцию") #+ "\n" + emoji.emojize(":books:"))
    myasks = telebot.types.KeyboardButton("Мои вопросы")  #+   emoji.emojize(":house:"))
    ask = telebot.types.KeyboardButton("Задать вопрос") #+   emoji.emojize(":question:"))
    answer = telebot.types.KeyboardButton("Ответить на вопрос") #+ "\n" + emoji.emojize(":bulb:"))
    markup.add(addSkill, ask, answer,myasks)
    return markup

# def saveSession(id,session):
#     db.saveSession(id,session)
#
def loadSession(id):
    data = db.loadSession(id)
    user =  User(id)
    user.importSession(data)
    return user



bot.polling()
