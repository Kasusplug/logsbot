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
    log_processing = subprocess.Popen(["go", "run", r"C:\Users\kasus\Desktop\pythonapps\logsbot\go_logger\task.go"])


def stop_generation_logs():
    global log_processing
    if log_processing:
        log_processing.terminate()  
        log_processing.wait()  
        log_processing = None


#в исходном коде го логи обновляются бесконечно c учетом моего кода здесь для более  рандомной генерации добавлено ожидание 
def delayed_stop_logs(chat_id):
    time.sleep(5)
    stop_generation_logs()
    bot.send_message(chat_id, 'Генерация логов завершена.')


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f'Hello!, {message.from_user.username}, this bot was created to easily control all logs')


@bot.message_handler(commands=['test'])
def test(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Сгенерировать логи', callback_data="generate_logs"))
    bot.send_message(message.chat.id, f'Для генерации логов нажмите на кнопку.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "generate_logs")
def handle_logs(call):
    start_generation_logs()
    bot.send_message(call.message.chat.id, "Логи генерируются.....")
    threading.Thread(target=delayed_stop_logs, args=(call.message.chat.id,)).start()


bot.polling()