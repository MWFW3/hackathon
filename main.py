import telebot
from UserModule import User
bot = telebot.TeleBot('1408437105:AAERPrZPLbkGoHN9HzObvYScyGBQNbwZzoY')

dictUser={}
comps=["программирование", "unix", "программная инжнерия", "ВСЁ ВЫБРАЛ"]

@bot.message_handler(commands=['start'])
def start(message):
    user=User(message.chat.username)
    dictUser[message.chat.id]=user
    msg="Приветствую тебя студент, здесь ты можешь задавать вопросы другим студентам или отвечать сам на то, в чём разбираешься."
    msg+="Нажми \"добавить компетенцию\", чтобы указать, чем владеешь или сразу задай вопрос"
    bot.send_message(message.chat.id, msg, reply_markup=drawMainMenu())

#----------------------------------------------------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Добавить компетенцию")
def addComp(message):
    dictUser[message.chat.id].inChoose=True
    msg="Выбирайте:"
    markup = telebot.types.ReplyKeyboardMarkup()
    for i in comps:
        markup.add(telebot.types.KeyboardButton(i))
    bot.send_message(message.chat.id, msg, reply_markup=markup)
    print(dictUser[message.chat.id].name)
    print(dictUser[message.chat.id].inChoose)

@bot.message_handler(func=lambda message: message.text == "ВСЁ ВЫБРАЛ")
def finishChoose(message):
    if dictUser[message.chat.id].inChoose:
        dictUser[message.chat.id].inChoose=False
    msg="Спасибо, вы выбрали компетенции"
    bot.send_message(message.chat.id, msg, reply_markup=drawMainMenu())
    print(dictUser[message.chat.id].name)

#----------------------------------------------------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == "Задать вопрос")
def ask(message):
    dictUser[message.chat.id].waitingForQuestion=True

@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, "reseted", reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text !=" ")
def hadlerOfAny(message):
    msg="-"
    if dictUser[message.chat.id].inChoose:
        for i in comps:
            if i==message.text:
                dictUser[message.chat.id].Comps.append(i)
                break
        print(dictUser[message.chat.id].name)
        print(dictUser[message.chat.id].Comps)
    if dictUser[message.chat.id].waitingForQuestion:
        Question=message.text
        

def drawMainMenu():
    markup = telebot.types.ReplyKeyboardMarkup()
    addSkill = telebot.types.KeyboardButton("Добавить компетенцию")
    ask = telebot.types.KeyboardButton("Задать вопрос")
    answer = telebot.types.KeyboardButton("Ответить на вопрос")
    markup.add(addSkill, ask, answer)
    return markup

bot.polling()