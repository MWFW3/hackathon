import telebot
bot = telebot.TeleBot('1408437105:AAERPrZPLbkGoHN9HzObvYScyGBQNbwZzoY')

comps=["программирование", "unix", "программная инжнерия", ]

@bot.message_handler(commands=['start'])
def start(message):
    msg="Приветствую тебя студент, здесь ты можешь задавать вопросы другим студентам или отвечать сам на то, в чём разбираешься."
    msg+="Нажми \"добавить компетенцию\", чтобы указать, чем владеешь или сразу задай вопрос"
    markup=telebot.types.ReplyKeyboardMarkup()
    addSkill=telebot.types.KeyboardButton("Добавить компетенцию")
    ask=telebot.types.KeyboardButton("Задать вопрос")
    markup.add(addSkill,ask)
    bot.send_message(message.chat.id, msg, reply_markup=markup)



bot.polling()