import telebot
from dotenv import load_dotenv
import os
from telebot import types
import subprocess
import time
import threading
import psutil
from whole_outputs import info_output, error_output, debug_output

load_dotenv(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\data.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

#переменная в которой работает процесс с файлом голанг на всех этапах
log_processing = None


class Logs:

    def __init__(self, file_name_read, file_name_record):
        self.file_name_read = file_name_read
        self.file_name_record = file_name_record
        self.logs_time_count_info = {}
        self.logs_time_count_error = {}
        self.logs_time_count_debug = {}
        self.count_info = {msg: 0 for msg in info_output}
        self.count_error = {msg: 0 for msg in error_output}
        self.count_debug = {msg: 0 for msg in debug_output}

    def logs_find(self):
        with open(self.file_name_read, 'r', encoding='utf-8') as logs_events:
            with open(self.file_name_record, 'w', encoding='utf-8') as new_logs:        
                for line in logs_events:
                    line = line.strip()
                    if "[INFO]" in line:
                        timestamp = line[0:90] 
                        if timestamp in self.logs_time_count_info:
                            self.logs_time_count_info[timestamp] += 1  
                        else:
                            self.logs_time_count_info[timestamp] = 1  
                        new_logs.write(line + '\n')
                    elif "[ERROR]" in line:
                        timestamp = line[0:90]
                        if timestamp in self.logs_time_count_error:
                            self.logs_time_count_error[timestamp] += 1  
                        else:
                            self.logs_time_count_error[timestamp] = 1  
                        new_logs.write(line + '\n')
                    elif "[DEBUG]" in line:
                        timestamp = line[0:90]
                        if timestamp in self.logs_time_count_debug:
                            self.logs_time_count_debug[timestamp] += 1  
                        else:
                            self.logs_time_count_debug[timestamp] = 1  
                        new_logs.write(line + '\n')
                print('Successfully processed all logs')
    
    def logs_counter(self):
        with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\catched_logs.log', 'w', encoding='utf-8') as new_logs:
            for timestamp, count in self.logs_time_count_info.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            for timestamp, count in self.logs_time_count_error.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            for timestamp, count in self.logs_time_count_debug.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            print('Succesfully counted ALL logs')


    def logs_compile(self):
        with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\catched_logs.log', 'r', encoding='utf-8') as read_logs:
            with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\counted.log', 'w', encoding='utf-8') as counted_logs:
                for line in read_logs:
                    line = line.strip()

                    for info in info_output:
                        if info in line:
                            self.count_info[info] += 1
                    for error in error_output:
                        if error in line:
                            self.count_error[error] += 1
                    for debug in debug_output:
                        if debug in line:
                            self.count_debug[debug] += 1

                counted_logs.write("INFO logs count:\n")
                for info, count in self.count_info.items():
                    counted_logs.write(f"{info}: {count}\n")

                counted_logs.write("\nERROR logs count:\n")
                for error, count in self.count_error.items():
                    counted_logs.write(f"{error}: {count}\n")

                counted_logs.write("\nDEBUG logs count:\n")
                for debug, count in self.count_debug.items():
                    counted_logs.write(f"{debug}: {count}\n")

        print("whole outputs was counted successfully and written to file")


    def error_logs_write(self):
        with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\catched_logs.log', 'r', encoding='utf-8') as read_logs:
            with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\error.log', 'w', encoding='utf-8') as error_logs:
                for error_log in read_logs:
                    if '[ERROR]' in error_log:
                        error_logs.write(error_log)


    def counted_error_logs_write(self):
        with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\counted.log', 'r', encoding='utf-8') as counted_logs:
            with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\error_counted.log', 'w', encoding='utf-8') as error_counted_logs:
                for error_log in counted_logs:
                    if '[ERROR]' in error_log:
                        error_counted_logs.write(error_log)




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


def create_log_buttons(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Показать все логи', callback_data="show_all"),
        types.InlineKeyboardButton('Показать количество логов', callback_data="show_counted"),
        types.InlineKeyboardButton('Показать только логи error', callback_data="show_error"),
        types.InlineKeyboardButton('Показать количество логов error', callback_data="show_counted_error")
    )
    bot.send_message(chat_id, 'Выберите опцию:', reply_markup=markup)


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


@bot.message_handler(commands=['count'])
def count(message):
    check_logs = Logs(
    file_name_read=r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\logs.log',
    file_name_record=r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\catched_logs.log'
)

    check_logs.logs_find()
    check_logs.logs_counter()
    check_logs.logs_compile()
    check_logs.error_logs_write()
    check_logs.counted_error_logs_write()
    markup = types.InlineKeyboardMarkup()
    markup.add(
    types.InlineKeyboardButton('Показать все логи', callback_data="show_all"),
    types.InlineKeyboardButton('Показать количество логов', callback_data="show_counted"),
    types.InlineKeyboardButton('Показать только логи error', callback_data="show_error"),
    types.InlineKeyboardButton('Показать количество логов error', callback_data="show_counted_error")
)
    bot.send_message(message.chat.id, 'Все подсчеты логов выполнены', reply_markup=markup)


@bot.callback_query_handler(func= lambda call: True)
def handle_query(call):
    try:
        if call.data == "show_all":
            with open(r'C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\catched_logs.log', 'r') as catched_logs:
                logs = catched_logs.read()
                bot.send_message(call.message.chat.id, logs)
    
        elif call.data == "show_counted":
            with open(r"C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\counted.log", 'r') as counted_logs:
                logs = counted_logs.read()
                bot.send_message(call.message.chat.id, logs)
        
        elif call.data == "show_error":
            with open(r"C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\error.log", 'r') as error_logs:
                logs = error_logs.read()
                bot.send_message(call.message.chat.id, logs)

        elif call.data == "show_counted_error":
            with open(r"C:\Users\kasus\Desktop\pythonapps\logsbot\task_1try\error_counted.log", 'r') as error_counted:
                logs = error_counted.read()
                bot.send_message(call.message.chat.id, logs)

        create_log_buttons(call.message.chat.id)

        bot.answer_callback_query(call.id)

    except Exception as e:
        bot.send_message(call.message.chat.id, f'Ошибка: {e}')

bot.polling()