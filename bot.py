import telebot
import time
import json
import os
import re
import random
import requests

from telebot import types
from datetime import datetime, date, timedelta


token = os.environ.get('bot_token')
remotely = os.environ.get('remotely')
remotely = int(remotely)
bot = telebot.TeleBot(str(token))
print('Бот работает!')

days_count = ['1', '2', '3', '4', '5', '6', '7']

data_loads = json.load(open('./schedule.json'))
data = json.dumps(data_loads)
json_data = json.loads(data)

data_loads3 = json.load(open('./schedule_next_day.json'))
data3 = json.dumps(data_loads3)
json_data3 = json.loads(data3)


@bot.message_handler(commands = ['start'])
def start_command(message):
    str_countes = ''
    countes = [f'{message.from_user.id} — ID,\n',
               f'{message.from_user.first_name} — имя,\n',
               f'{message.from_user.last_name} — фамилия,\n',
               f'{message.from_user.username} — username.'
              ]
    for x in countes:
        str_countes += x
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    button = types.KeyboardButton(text = "Расписание на сегодня")
    button1 = types.KeyboardButton(text = "Расписание на завтра")
    button2 = types.KeyboardButton(text = "О нас")
    button3 = types.KeyboardButton(text = "Полное расписание")
    keyboard.row(button, button1)
    keyboard.row(button2, button3)
    bot.send_message(655041562, f'У тебя +1 новый пользователь! \n{str_countes}')
    bot.reply_to(message, "*Рад тебя видеть!* \n\nПропиши /schedule, или воспользуйся клавиатурой ниже! Если вдруг ты заблудился или забыл команды (со всеми бывает, не переживай) — /help в помощь.", parse_mode = 'Markdown', reply_markup = keyboard)
    


@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.reply_to(message, "Привет! Рад, что ты заглянул(а) сюда \n• /schedule — узнать расписание;"
                                                               "\n• /schedule_next — расписание на завтра;"
                                                               "\n• /schedule [цифра] — расписание для конкретного дня недели.")

@bot.message_handler(commands = ['schedule_full'])
def schedule_full(message):
    even_numbered_week = open('./Schedule/ИСиП-42. Чётная неделя.pdf', 'rb')
    odd_week = open('./Schedule/ИСиП-42. Нечётная неделя.pdf', 'rb')
    bot.send_message(message.chat.id, '📋 Расписание на *чётную* неделю:', parse_mode = 'Markdown')
    bot.send_document(message.chat.id, even_numbered_week)
    bot.send_message(message.chat.id, '📋 Расписание на *нечётную* неделю:', parse_mode = 'Markdown')
    bot.send_document(message.chat.id, odd_week)
    even_numbered_week.close()
    odd_week.close()
    
@bot.message_handler(commands = ['schedule'])
def schedule(message):
    if message.text == '/schedule':
        delta = timedelta(hours = 3)
        now = datetime.now() + delta
        days_int = now.isoweekday()
        
        sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
        d1 = sep - timedelta(days = sep.weekday())
        d2 = now - timedelta(days = now.weekday())
        parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
        
        if parity == 0:
            schedule_days_int = json_data["Для нечётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            if remotely == 1:
                schedule = re.sub("Аудитория: \d\d\d", "Аудитория: Дистанционно.", schedule)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "О нас")
            button3 = types.KeyboardButton(text = "Полное расписание")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            if remotely == 1:
                schedule = re.sub("\d\d\d", "Дистанционно.", schedule)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "О нас")
            button3 = types.KeyboardButton(text = "Полное расписание")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        try:
            delta = timedelta(hours = 3)
            now = datetime.now() + delta
            days_int = now.isoweekday()

            sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
            d1 = sep - timedelta(days = sep.weekday())
            d2 = now - timedelta(days = now.weekday())
            parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная

            if parity == 0:
                schedule_days_int = json_data["Для нечётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(message.text[10:])
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', 'для этой недели')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
                button = types.KeyboardButton(text = "Расписание на сегодня")
                button1 = types.KeyboardButton(text = "Расписание на завтра")
                button2 = types.KeyboardButton(text = "О нас")
                button3 = types.KeyboardButton(text = "Полное расписание")
                keyboard.row(button, button1)
                keyboard.row(button2, button3)
                bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
            else:
                schedule_days_int = json_data["Для чётной недели"]
                schedule = ''
                for x in schedule_days_int:
                    keys = schedule_days_int.get(message.text[10:])
                schedule += str(keys)
                schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', 'для этой недели')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
                button = types.KeyboardButton(text = "Расписание на сегодня")
                button1 = types.KeyboardButton(text = "Расписание на завтра")
                button2 = types.KeyboardButton(text = "О нас")
                button3 = types.KeyboardButton(text = "Полное расписание")
                keyboard.row(button, button1)
                keyboard.row(button2, button3)
                if schedule == '':
                    schedule = "Упс, но ты ввёл что-то не так."
                bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)   
        except:
            bot.send_message(message.chat.id, 'Так. Тут что-то не так. \nВведи числа (от 1 до 7), либо обратись к @whomet.')                
        
@bot.message_handler(commands = ['schedule_next'])
def schedule_next(message):
    delta = timedelta(hours = 3)
    delta1 = timedelta(days = 1)
    now = datetime.now() + delta
    now_next = datetime.now() + delta + delta1
    days_int = now.isoweekday()
    
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
    d1 = sep - timedelta(days = sep.weekday())
    d2 = now - timedelta(days = now.weekday())
    parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
    
    if days_int == 7:
        days_print = 0
        if parity == 0:
            parity = 1
        else:
            parity = 0
    else:
        days_print = days_int
    
        
    if parity == 0:
        schedule_days_int = json_data3["Для нечётной недели"]
        schedule = ''
        for x in schedule_days_int:
            keys = schedule_days_int.get(str(days_print))
        nowtime = now_next.strftime("(%d.%m.%y)")
        schedule += str(keys)
        schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
        if remotely == 1:
            schedule = re.sub("\d\d\d", "Дистанционно", schedule)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "О нас")
        button3 = types.KeyboardButton(text = "Полное расписание")
        keyboard.row(button, button1)
        keyboard.row(button2, button3)
        bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    else:
        schedule_days_int = json_data3["Для чётной недели"]
        schedule = ''
        for x in schedule_days_int:
            keys = schedule_days_int.get(str(days_print))
        nowtime = now_next.strftime("(%d.%m.%y)")
        schedule += str(keys)
        schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
        if remotely == 1:
            schedule = re.sub("\d\d\d", "Дистанционно", schedule)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        button = types.KeyboardButton(text = "Расписание на сегодня")
        button1 = types.KeyboardButton(text = "Расписание на завтра")
        button2 = types.KeyboardButton(text = "О нас")
        button3 = types.KeyboardButton(text = "Полное расписание")
        keyboard.row(button, button1)
        keyboard.row(button2, button3)
        bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)


@bot.message_handler(content_types = ['text'])
def text(message):
    if message.text.lower() == 'расписание на сегодня':
        delta = timedelta(hours = 3)
        now = datetime.now() + delta
        days_int = now.isoweekday()
        
        sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
        d1 = sep - timedelta(days = sep.weekday())
        d2 = now - timedelta(days = now.weekday())
        parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
        
        if parity == 0:
            schedule_days_int = json_data["Для нечётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "О нас")
            button3 = types.KeyboardButton(text = "Полное расписание")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_int))
            nowtime = now.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "О нас")
            button3 = types.KeyboardButton(text = "Полное расписание")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text.lower() == 'расписание на завтра':
        delta = timedelta(hours = 3)
        delta1 = timedelta(days = 1)
        now = datetime.now() + delta
        now_next = datetime.now() + delta + delta1
        days_int = now.isoweekday()
        
        sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
        d1 = sep - timedelta(days = sep.weekday())
        d2 = now - timedelta(days = now.weekday())
        parity = ((d2 - d1).days // 7) % 2 #возвращает 0, если неделя нечётная и 1, если чётная
        
        if days_int == 7:
            days_print = 0
            if parity == 0:
                parity = 1
            else:
                parity = 0
        else:
            days_print = days_int
        
        
        if parity == 0:
            schedule_days_int = json_data3["Для нечётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_print))
            nowtime = now_next.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "О нас")
            button3 = types.KeyboardButton(text = "Полное расписание")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
        else:
            schedule_days_int = json_data3["Для чётной недели"]
            schedule = ''
            for x in schedule_days_int:
                keys = schedule_days_int.get(str(days_print))
            nowtime = now_next.strftime("(%d.%m.%y)")
            schedule += str(keys)
            schedule = schedule.replace("['", '').replace("']", '').replace(r'\n', '\n').replace("', '", '').replace('()', nowtime)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            button = types.KeyboardButton(text = "Расписание на сегодня")
            button1 = types.KeyboardButton(text = "Расписание на завтра")
            button2 = types.KeyboardButton(text = "О нас")
            button3 = types.KeyboardButton(text = "Полное расписание")
            keyboard.row(button, button1)
            keyboard.row(button2, button3)
            bot.send_message(message.chat.id, schedule, parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text.lower() == 'о нас':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text = "📝 Написать разработчику", url = 'https://t.me/ppippette')
        keyboard.add(button)
        bot.send_message(message.chat.id, '*Наша команда* \n\n🧑‍💻 *Разработчик:* @ppippette \n🛠 *Тестировщик:* @whomet \n👉 *Наш Github:* https://github.com/GRTUBORG/isip-42 \n\n• Обо всех _ошибках_, _проблемах_ и Ваших _гениальных идеях_ просьба писать *разработчику* ✍️ \n• *Обновление было:* 17.01.22, v. 2.0', parse_mode = 'Markdown', reply_markup = keyboard)
    elif message.text.lower() == 'полное расписание':
        even_numbered_week = open('./Schedule/ИСиП-42. Чётная неделя.pdf', 'rb')
        odd_week = open('./Schedule/ИСиП-42. Нечётная неделя.pdf', 'rb')
        bot.send_message(message.chat.id, '📋 Расписание на *чётную* неделю:', parse_mode = 'Markdown')
        bot.send_document(message.chat.id, even_numbered_week)
        bot.send_message(message.chat.id, '📋 Расписание на *нечётную* неделю:', parse_mode = 'Markdown')
        bot.send_document(message.chat.id, odd_week)
        even_numbered_week.close()
        odd_week.close()

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
