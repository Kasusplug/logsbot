import telebot
from dotenv import load_dotenv
import os
from telebot import types
import subprocess
import time
import threading

load_dotenv(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\data.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

log_processing = None


def start_generation_logs():
    global log_processing
    log_processing = subprocess.Popen(["go", "run", "C:\Users\kasus\Desktop\pythonapps\logsbot\go_logger\task.go"])


def stop_generation_logs():
    global log_processing
    if log_processing:
        log_processing.terminate()
        log_processing = None


#в исходном коде го логи генерируются бесконечно, здесь ограничение на 15 секунд
def delayed_stop_logs():
    time.sleep(15)
    stop_generation_logs()


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f'Hello!, {message.from_user.username}')


@bot.message_handler(commands=['test'])
def test(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Сгенерировать логи', callback_data="generate_logs"))
    bot.send_message(message.chat.id, f'Для генерации логов нажмите на кнопку.', reply_markup=markup)

bot.polling()