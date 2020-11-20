import telebot
bot = telebot.TeleBot('1408437105:AAERPrZPLbkGoHN9HzObvYScyGBQNbwZzoY')

comps=["программирование", "unix", "программная инжнерия", "ВСЁ ВЫБРАЛ"]
inChoose=False

@bot.message_handler(commands=['start'])
def start(message):
    msg="Приветствую тебя студент, здесь ты можешь задавать вопросы другим студентам или отвечать сам на то, в чём разбираешься."
    msg+="Нажми \"добавить компетенцию\", чтобы указать, чем владеешь или сразу задай вопрос"
    bot.send_message(message.chat.id, msg, reply_markup=drawMainMenu())
    print(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Добавить компетенцию")
def addComp(message):
    msg="Выбирайте:"
    markup = telebot.types.ReplyKeyboardMarkup()
    btns=[]
    for i in comps:
        markup.add(telebot.types.KeyboardButton(i))
    bot.send_message(message.chat.id, msg, reply_markup=markup)
    inChoose=True;

@bot.message_handler(func=lambda message: message.text == "ВСЁ ВЫБРАЛ")
def finishChoose(message):
    msg="Спасибо, вы выбрали компетенции"
    bot.send_message(message.chat.id, msg, reply_markup=drawMainMenu())
    inChoose=True;

@bot.message_handler(func=lambda message: message.text !=" ")
def hadlerOfAny(message):
    msg="-"
    for i in comps:
        if i==message.text:
            msg="+"
            break
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['reset'])
def reset(message):
    bot.send_message(message.chat.id, "reseted", reply_markup=telebot.types.ReplyKeyboardRemove())

def drawMainMenu():
    markup = telebot.types.ReplyKeyboardMarkup()
    addSkill = telebot.types.KeyboardButton("Добавить компетенцию")
    ask = telebot.types.KeyboardButton("Задать вопрос")
    markup.add(addSkill, ask)
    return markup

bot.polling()