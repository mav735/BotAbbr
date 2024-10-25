import telebot
import time
from requests.exceptions import RequestException

bot = telebot.TeleBot('7060695421:AAGhq8DTppMGjYsf197ZWJAzCA01Iqpydec')

with open('abbr.txt', 'r', encoding='UTF-8') as f:
    abbrs = f.read().split('\n')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! \n'
                                'Я - бот-Вордбук 🤖\n'
                                '- твой интеллектуальный помощник в распознавании аббревиатур.\n \n'
                                'Помогу быстро найти значения различных сокращений и аббревиатур, используемых в рабочем процессе. \n'
                                'Бот-словарь станет надежным спутником в рабочем процессе, облегчая коммуникацию и повышая эффективность взаимодействия с коллегами и смежными подразделениями💯')
    bot.send_message(m.chat.id, 'Введите аббревиатуру, значение которой хотите узнать👇')

@bot.message_handler(commands=["send_abbr_file"])
def send_abbr_file(m):
    if m.chat.id == 431436587:
        with open('abbr.txt', 'rb') as file:
            bot.send_document(m.chat.id, file)
    else:
        bot.send_message(m.chat.id, "Извините, у вас нет доступа к этой команде.")

@bot.message_handler(content_types=['document'])
def receive_abbr_file(message):
    if message.chat.id == 431436587 and message.document.file_name == 'abbr.txt':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('abbr.txt', 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Файл abbr.txt был успешно обновлен!")
        reload_abbrs()

def reload_abbrs():
    global abbrs
    with open('abbr.txt', 'r', encoding='UTF-8') as f:
        abbrs = f.read().split('\n')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        index_start = abbrs.index(message.text.lower())
        try:
            index_stop = abbrs.index('', index_start)
            need_part = abbrs[index_start + 1:index_stop + 1]
            new_message = '\n'.join(need_part)
        except ValueError:
            new_message = abbrs[index_start + 1]
        bot.send_message(message.from_user.id, new_message)
    except ValueError:
        chat_id = 431436587
        bot.send_message(message.from_user.id, 'Я не знаю такой аббревиатуры😞 \n'
                                               'Но уже отправил Ваш запрос создателю бота для пополнения базы знаний!')
        bot.send_message(chat_id, 'Пользователь пытался найти аббревиатуру: ' + message.text)

bot.polling(none_stop=True, interval=0)

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except RequestException as err:
        print(err)
        print('* Connection failed, waiting to reconnect...')
        time.sleep(15)
        print('* Reconnecting.')
