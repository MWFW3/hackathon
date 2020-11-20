import telebot
bot = telebot.TeleBot('1408437105:AAERPrZPLbkGoHN9HzObvYScyGBQNbwZzoY')

comps=["программирование", "unix", "программная инжнерия", ]

@bot.message_handler(commands=['start'])
def start(message):
    msg="Приветствую тебя студент, здесь ты можешь задавать вопросы другим студентам или отвечать сам на то, в чём разбираешься."
    msg+="Нажми \"добавить компетенцию\", чтобы указать, чем владеешь или сразу задай вопрос"
    markup=telebot.types.InlineKeyboardMarkup()
    addSkill=telebot.types.InlineKeyboardButton("Добавить компетенцию",callback_data="/addComp")
    ask=telebot.types.InlineKeyboardButton("Задать вопрос", callback_data="/ask")
    markup.add(addSkill,ask)
    bot.send_message(message.chat.id, msg, reply_markup=markup)



bot.polling()