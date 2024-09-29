import telebot
from dotenv import load_dotenv
import os
from telebot import types
import subprocess
import time
import threading
import psutil
from new_parser import Logs

load_dotenv(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\data.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

#переменная в которой работает процесс с файлом голанг на всех этапах
log_processing = None

#стартуем файл го 
def start_generation_logs():
    global log_processing
    log_processing = subprocess.Popen(["go", "run", r"C:\Users\kasus\Desktop\pythonapps\logsbot\go_logger\task.go"])

#завершаем родительские и дочерние процессы(без этой функции код го работает бесконечно)
def stop_generation_logs():
    global log_processing
    if log_processing:
        parent = psutil.Process(log_processing.pid)

        for child in parent.children(recursive=True):
            child.kill()

        log_processing.kill()
        log_processing.wait()

        log_processing = None


#для более рандомной генерации добавлено ожидание 
def delayed_stop_logs(chat_id):
    time.sleep(5)
    stop_generation_logs()
    bot.send_message(chat_id, 'Генерация логов завершена.')


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f"Привет!, {message.from_user.username} \n"
                    "Этот бот разработан специально для команды ВК=)\n"
                    "В данном боте доступны команды для получения логов и статистики по ним\n"
                    "На данный момент доступны следующие комманды:\n"
                    "/start - команда которая вызывает данное сообщение\n"
                    "/generate - пока что генерирует логи\n"
                    "/count - производит все операции по подсчету и компиляции всех вариантов логов \n"
                    "/show_all - показывает все логи\n"
                    "/show_counted - показывает все логи по их количеству в генерации\n"
                    "/show_error - показывает только логи с тегом error\n"
                    "/show_counted_error - показывает посчитанные логи с тегом error\n")


@bot.message_handler(commands=['generate'])
def generate(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Сгенерировать логи', callback_data="generate_logs"))
    bot.send_message(message.chat.id, f'Для генерации логов нажмите на кнопку.', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "generate_logs")
def handle_logs(call):
    start_generation_logs()
    bot.send_message(call.message.chat.id, "Логи генерируются.....")
    threading.Thread(target=delayed_stop_logs, args=(call.message.chat.id,)).start()


# @bot.message_handler(commands=['count'])
# def count(message):
#     check_logs = Logs(
#     file_name_read=r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\logs.log',
#     file_name_record=r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\catched_logs.log'
# )

#     check_logs.logs_find()
#     check_logs.logs_counter()
#     check_logs.logs_compile()
#     check_logs.error_logs_write()
#     check_logs.counted_error_logs_write()
#     markup_show_all = types.InlineKeyboardMarkup()
#     markup_show_counted = types.InlineKeyboardMarkup()
#     markup_show_error = types.InlineKeyboardMarkup()
#     markup_show_counted_error = types.InlineKeyboardMarkup()
#     markup_show_all.add(types.InlineKeyboardButton('Показать все логи', callback_data="show_all"))
#     markup_show_counted.add(types.InlineKeyboardButton('Показать количество логов', callback_data="show_all"))
#     markup_show_error.add(types.InlineKeyboardButton('Показать только логи error', callback_data="show_all"))
#     markup_show_counted_error.add(types.InlineKeyboardButton('Показать количество логов error', callback_data="show_all"))
#     bot.send_message(message.chat.id, 'Все подсчеты логов выполнены', reply_markup=[markup_show_all, markup_show_counted, markup_show_counted_error, markup_show_error])


bot.polling()