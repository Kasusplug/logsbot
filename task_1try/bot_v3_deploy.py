import telebot
from dotenv import load_dotenv
import os
from telebot import types
import subprocess
import time
import threading
import psutil
from whole_outputs import info_output, error_output, debug_output

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Переменная, в которой работает процесс с файлом Go на всех этапах
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
            with open(self.file_name_record, 'w',
                      encoding='utf-8') as new_logs:
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
        with open(os.path.join(os.getcwd(), 'catched_logs.log'),
                  'w',
                  encoding='utf-8') as new_logs:
            for timestamp, count in self.logs_time_count_info.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            for timestamp, count in self.logs_time_count_error.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            for timestamp, count in self.logs_time_count_debug.items():
                new_logs.write(f"  {timestamp} - {count}" + '\n')
            print('Successfully counted ALL logs')

    def logs_compile(self):
        with open(os.path.join(os.getcwd(), 'catched_logs.log'),
                  'r',
                  encoding='utf-8') as read_logs:
            with open(os.path.join(os.getcwd(), 'counted.log'),
                      'w',
                      encoding='utf-8') as counted_logs:
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

        print("Whole outputs were counted successfully and written to file")

    def error_logs_write(self):
        with open(os.path.join(os.getcwd(), 'catched_logs.log'),
                  'r',
                  encoding='utf-8') as read_logs:
            with open(os.path.join(os.getcwd(), 'error.log'),
                      'w',
                      encoding='utf-8') as error_logs:
                for error_log in read_logs:
                    if '[ERROR]' in error_log:
                        error_logs.write(error_log)

    def counted_error_logs_write(self):
        with open(os.path.join(os.getcwd(), 'counted.log'),
                  'r',
                  encoding='utf-8') as counted_logs:
            with open(os.path.join(os.getcwd(), 'error_counted.log'),
                      'w',
                      encoding='utf-8') as error_counted_logs:
                for error_log in counted_logs:
                    if '[ERROR]' in error_log:
                        error_counted_logs.write(error_log)


# Стартуем файл Go
def start_generation_logs():
    global log_processing
    log_processing = subprocess.Popen(
        ["go", "run",
         os.path.join(os.getcwd(), 'go_logger/task.go')])


# Завершаем родительские и дочерние процессы (без этой функции код Go работает бесконечно)
def stop_generation_logs():
    global log_processing
    if log_processing:
        parent = psutil.Process(log_processing.pid)

        for child in parent.children(recursive=True):
            child.kill()

        log_processing.kill()
        log_processing.wait()

        log_processing = None


# Для более рандомной генерации добавлено ожидание
def delayed_stop_logs_and_update(chat_id):
    time.sleep(5)
    stop_generation_logs()
    bot.send_message(chat_id, 'Генерация логов завершена.')

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Сгенерировать логи',
                                   callback_data="generate_logs"),
        types.InlineKeyboardButton('Подсчитать логи',
                                   callback_data="count_logs"))
    bot.send_message(chat_id,
                     "Логи сгенерированы. Выберите действие:",
                     reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Сгенерировать логи',
                                   callback_data="generate_logs"),
        types.InlineKeyboardButton('Подсчитать логи',
                                   callback_data="count_logs"))
    bot.send_message(
        message.chat.id, f"Привет!, {message.from_user.username} \n"
        "Этот бот разработан специально для команды ВК=)\n"
        "В данном боте доступны команды для получения логов и статистики по ним\n"
        "Для работы с ботом для начала нужно сгенерировать логи, далее воспользоваться коммандой /count или нажать кнопку посчитать логи\n"
        "Доступны следующие команды:\n"
        "/start - команда которая вызывает данное сообщение\n"
        "/generate - генерирует новые логи\n"
        "/count - производит все операции по подсчету и компиляции всех вариантов логов \n"
        "/show_all - показывает все логи\n"
        "/show_counted - показывает все логи по их количеству в генерации\n"
        "/show_error - показывает только логи с тегом error\n"
        "/show_counted_error - показывает посчитанные логи с тегом error\n",
        reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "generate_logs")
def handle_logs(call):
    start_generation_logs()
    bot.send_message(call.message.chat.id, "Логи генерируются.....")
    threading.Thread(target=delayed_stop_logs_and_update,
                     args=(call.message.chat.id, )).start()


@bot.callback_query_handler(func=lambda call: call.data == "count_logs")
def handle_count_logs(call):
    count(call.message)


@bot.message_handler(commands=['generate'])
def generate(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Сгенерировать логи',
                                   callback_data="generate_logs"))
    bot.send_message(message.chat.id,
                     f'Для генерации логов нажмите на кнопку.',
                     reply_markup=markup)


@bot.message_handler(commands=['count'])
def count(message):
    log_file_path = os.path.join(os.getcwd(), 'task_1try', 'logs.log')

    if not os.path.exists(log_file_path):
        bot.send_message(message.chat.id, f"Файл {log_file_path} не найден.")
        return

    check_logs = Logs(file_name_read=log_file_path,
                      file_name_record=os.path.join(os.getcwd(),
                                                    'catched_logs.log'))

    check_logs.logs_find()
    check_logs.logs_counter()
    check_logs.logs_compile()
    check_logs.error_logs_write()
    check_logs.counted_error_logs_write()
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('Показать все логи',
                                   callback_data="show_all"),
        types.InlineKeyboardButton('Показать количество логов',
                                   callback_data="show_counted"),
        types.InlineKeyboardButton('Показать только логи error',
                                   callback_data="show_error"),
        types.InlineKeyboardButton('Показать количество логов error',
                                   callback_data="show_counted_error"))
    bot.send_message(message.chat.id,
                     'Все подсчеты логов выполнены',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('Показать все логи',
                                       callback_data="show_all"),
            types.InlineKeyboardButton('Показать количество логов',
                                       callback_data="show_counted"),
            types.InlineKeyboardButton('Показать только логи error',
                                       callback_data="show_error"),
            types.InlineKeyboardButton('Показать количество логов error',
                                       callback_data="show_counted_error"))

        if call.data == "show_all":
            with open(os.path.join(os.getcwd(), 'catched_logs.log'),
                      'r',
                      encoding='utf-8') as logs:
                log_data = logs.read()

                for i in range(0, len(log_data), 4096):
                    bot.send_message(call.message.chat.id,
                                     log_data[i:i + 4096])
            bot.send_message(call.message.chat.id,
                             "Выберите следующее действие:",
                             reply_markup=markup)

        elif call.data == "show_counted":
            with open(os.path.join(os.getcwd(), 'counted.log'),
                      'r',
                      encoding='utf-8') as counted_logs:
                counted_data = counted_logs.read()

                for i in range(0, len(counted_data), 4096):
                    bot.send_message(call.message.chat.id,
                                     counted_data[i:i + 4096])
            bot.send_message(call.message.chat.id,
                             "Выберите следующее действие:",
                             reply_markup=markup)

        elif call.data == "show_error":
            with open(os.path.join(os.getcwd(), 'error.log'),
                      'r',
                      encoding='utf-8') as error_logs:
                error_data = error_logs.read()

                for i in range(0, len(error_data), 4096):
                    bot.send_message(call.message.chat.id,
                                     error_data[i:i + 4096])
            bot.send_message(call.message.chat.id,
                             "Выберите следующее действие:",
                             reply_markup=markup)

        elif call.data == "show_counted_error":
            with open(os.path.join(os.getcwd(), 'error_counted.log'),
                      'r',
                      encoding='utf-8') as error_counted_logs:
                error_counted_data = error_counted_logs.read()

                for i in range(0, len(error_counted_data), 4096):
                    bot.send_message(call.message.chat.id,
                                     error_counted_data[i:i + 4096])
            bot.send_message(call.message.chat.id,
                             "Выберите следующее действие:",
                             reply_markup=markup)

    except Exception as e:
        bot.send_message(call.message.chat.id, str(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)
