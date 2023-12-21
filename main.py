import telebot
from telebot import types

bot = telebot.TeleBot("6453743339:AAELoAuShU3elB7Xum6FQdDXPcvbrKZpDwA")
store_id = None
command = 'a'

user_addresses = {}
available_addresses = ['Адрес 1', 'Адрес 2', 'Адрес 3']  # load from db


@bot.message_handler(commands=['start'])
def start(message):
    global command
    command = 'start'
    id = message.chat.id

    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    for address in available_addresses:
        markup.add(types.KeyboardButton(address))

    bot.send_message(id, "Выберите адрес из списка:", reply_markup=markup)
    user_addresses[id] = None  # Инициализируем адрес пользователя значением None


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    txt = message.text
    id = message.chat.id
    message_to_user = 'Неизвестная комманда'

    if command == 'start':
        if txt in available_addresses:
            user_addresses[id] = txt
            message_to_user = 'Записал!'
        else:
            message_to_user = 'Неверный адрес, выберите вариант из списка.'
    bot.send_message(id, message_to_user)


if __name__ == "__main__":
    bot.polling(none_stop=True)
