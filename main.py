import telebot
from telebot import types
from db import *

bot = telebot.TeleBot("6453743339:AAELoAuShU3elB7Xum6FQdDXPcvbrKZpDwA")
store_id = None
command = ''

user_addresses = {}
order_info = {'provider': '', 'title': '', 'value': ''}
available_addresses = None
available_storages = None
available_providers = None
available_titles = None


def request_start(id):
    message_to_user = 'Для начала введите адрес вашего магазина (команда /start)'
    bot.send_message(id, message_to_user)


def get_storage_buttons(id):
    global command
    global available_storages

    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    available_storages = load_storages(user_addresses[id])
    available_storages.append('Все склады')

    for store in available_storages:
        markup.add(types.KeyboardButton(store))

    return markup


def select_titles_value(id):
    global command

    command = 'select_titles_value'
    bot.send_message(id, 'Введите необходимое количество предметов:')


def request_provider(id):
    global command
    global available_providers
    command = 'provider'

    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    available_providers = load_providers(user_addresses[id])

    for provider in available_providers:
        markup.add(types.KeyboardButton(provider))

    bot.send_message(id, "Выберите поставщика, у которого необходимо сделать заказ:", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    global command
    global available_addresses
    command = 'start'
    id = message.chat.id

    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    available_addresses = load_addresses()
    for address in available_addresses:
        markup.add(types.KeyboardButton(address))

    bot.send_message(id, "Выберите адрес вашего магазина:", reply_markup=markup)
    user_addresses[id] = None  # Инициализируем адрес пользователя значением None


@bot.message_handler(commands=['check_items'])
def check_storage(message):
    global command
    command = 'check_items'

    id = message.chat.id
    markup = get_storage_buttons(id)

    bot.send_message(id, "Выберите склад, содержимое которого хотите посмотреть:", reply_markup=markup)


@bot.message_handler(commands=['check_machines'])
def check_machine(message):
    global command
    command = 'check_machines'

    id = message.chat.id
    markup = get_storage_buttons(id)

    bot.send_message(message.chat.id, "Выберите склад, оборудование которого хотите просмотреть:", reply_markup=markup)


@bot.message_handler(commands=['order'])
def order(message):
    global command
    global available_titles
    command = 'order'
    id = message.chat.id

    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    available_titles = get_titles_list(user_addresses[id])
    for address in available_titles:
        markup.add(types.KeyboardButton(address))

    bot.send_message(id, "Выберите нужное наименование:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    global command

    answer = message.text
    id = message.chat.id
    message_to_user = 'Неизвестная команда'

    if command == '':
        message_to_user = 'Во всех непонятных случаях используйте команду /start'
    if command == 'start':
        if answer in available_addresses:
            user_addresses[id] = answer
            message_to_user = 'Записал!'
        else:
            message_to_user = 'Неверный адрес, выберите вариант из списка.'
    elif command == 'check_items':
        if answer in available_storages:
            message_to_user = show_storage_items_info(answer)
    elif command == 'check_machines':
        if answer in available_storages:
            message_to_user = show_storage_machines_info(answer)
    elif command == 'order':
        if answer in available_titles:
            order_info['title'] = answer
            select_titles_value(message.chat.id)
            return
    elif command == 'select_titles_value':
        order_info['value'] = int(answer)
        request_provider(message.chat.id)
        return
    elif command == 'provider':
        if answer in available_providers:
            order_info['provider'] = answer
            make_oder(user_addresses[id], order)

            print(order_info)
            message_to_user = 'Заказ сделан!'

    command = ''
    bot.send_message(id, message_to_user)


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass
