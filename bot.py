import datetime
import subprocess

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types

from parser_bot.cruds import Session

token = '6114556331:AAE9SNlPIKpgNdtaHYgAekvzAZounm4Yq4k'
bot = telebot.TeleBot(token)
ses = Session()

i = 1


def scrap():
    global i
    print(f"Парсинг запустился {i}й раз в")
    i += 1
    print(datetime.datetime.now())
    subprocess.call('scrapy crawl problems')


# Первый раз запускаем парсинг напрямую, далее это будет делать на фоне apscheduler
scrap()
sched = BackgroundScheduler()
sched.add_job(scrap, 'interval', hours=1)
sched.start()

print(datetime.datetime.now())


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Получить контест")
    btn2 = types.KeyboardButton("Найти задачу")
    keyboard.add(btn1, btn2)
    question = 'Здравствуйте! Чтобы Вы хотели, получить сгенерированную уникальную подборку задач(контест) ' \
               'или найти конкретную задачу по номеру или названию?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Получить контест":
        bot.send_message(message.from_user.id, "Введите, пожалуйста, тему для контеста.")
        bot.register_next_step_handler(message, get_rating)
    elif message.text == "Найти задачу":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("По номеру")
        btn2 = types.KeyboardButton("По названию")
        btn3 = types.KeyboardButton("В начало")
        keyboard.add(btn1, btn2, btn3)
        question = 'Как бы Вы хотели, найти задачу, по номеру или названию?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif message.text == "По номеру":
        bot.send_message(message.from_user.id, "Напишите, пожалуйста номер задачи.")
        bot.register_next_step_handler(message, find_problem_number)
    elif message.text == "По названию":
        bot.send_message(message.from_user.id, "Напишите, пожалуйста название задачи.")
        bot.register_next_step_handler(message, find_problem_name)
    elif message.text == "В начало":
        start(message)
    else:
        bot.send_message(message.from_user.id, "Я Вас не понимаю. Напишите /start или /help")


def get_rating(message):
    theme = message.text
    bot.send_message(message.from_user.id, "Введите сложность.")
    bot.register_next_step_handler(message, get_contest, theme)


def get_contest(message, theme):
    rating = message.text
    if rating.isnumeric():
        bot.send_message(message.from_user.id, ses.get_contest(theme, rating))
    else:
        bot.send_message(message.from_user.id, "Повторите ввод, пожалуйста.")
        bot.register_next_step_handler(message, get_contest, theme)


def find_problem_number(message):
    number = message.text
    bot.send_message(message.from_user.id, ses.find_problem_by_num(number))


def find_problem_name(message):
    name = message.text
    bot.send_message(message.from_user.id, ses.find_problem_by_name(name))


@bot.message_handler(commands=['/help'])
def start_contest(message):
    bot.send_message(message.from_user.id, "Я могу сгенерировать уникальную подборку задач(контест) ' \
                            'или найти конкретную задачу по номеру или названию.")


bot.polling(none_stop=True, interval=0)
