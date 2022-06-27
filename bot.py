from cgitb import reset
from email import message
from unittest import result
import telebot

from telebot import types
from search_by_wiki import getwiki, getwikisearch, getstr
from workwithdb import plus_user_query, show_top

bot = telebot.TeleBot('ur_BOT_TOKEN', parse_mode=None)

def create_keyboard_yesno():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_yes = types.KeyboardButton("Да") # кнопки
    key_no= types.KeyboardButton("Нет")
    keyboard.add(key_yes, key_no)
    return keyboard


def remove_keyboard():
    keyboard = types.ReplyKeyboardRemove(selective=False)
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет")
    elif message.text == "/wiki_search":
        wiki_search(message)
    elif message.text == "/top_query":
        bot.send_message(message.from_user.id, show_top())
    else:
        bot.reply_to(message, "Я тебя не понимаю. Напиши /help.")

#@bot.message_handler(commands=["Wiki_search"])
def wiki_search(message):
    bot.send_message(message.from_user.id, 'Отправьте мне слово, и я найду его значение на Wikipedia')
    # Получение сообщения от юзера
    bot.register_next_step_handler(message, handle_text)

#@bot.message_handler(content_types=["text"])
def handle_text(message):
    global results 
    results = getwikisearch(message.text)
    bot.send_message(message.from_user.id, results)

    if results == 'Ничего не нашлось\n':
        bot.send_message(message.from_user.id, 'Снова ищем?', reply_markup=create_keyboard_yesno())
        bot.register_next_step_handler(message, callback_worker)
    else:
        bot.send_message(message.from_user.id, 'Выберете что-то конкретное\n')
        bot.register_next_step_handler(message, searchbyresults)

def searchbyresults(message):
    i = message.text
    tmp = getstr(results, i)
    #print(tmp)
    if tmp == 'Введите заново:':
        bot.send_message(message.from_user.id, tmp)
        bot.register_next_step_handler(message, searchbyresults)
    else:    
        plus_user_query(tmp)

        # result = getwiki(tmp)
        bot.send_message(message.from_user.id, getwiki(tmp))

        bot.send_message(message.from_user.id, 'Снова ищем?', reply_markup=create_keyboard_yesno())

        bot.register_next_step_handler(message, callback_worker)


def callback_worker(message):
    if message.text == "Да":
        bot.send_message(message.from_user.id, 'Ладно\n',reply_markup=remove_keyboard())
        wiki_search(message)
    elif message.text == "Нет":
        bot.send_message(message.from_user.id, 'Ладно\n',reply_markup=remove_keyboard())



#bot.polling(none_stop=True, interval=0)
bot.infinity_polling()
