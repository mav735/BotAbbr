import json

import telebot
import time
from requests.exceptions import RequestException

bot = telebot.TeleBot('7060695421:AAGhq8DTppMGjYsf197ZWJAzCA01Iqpydec')
WAITING_FOR_ABBR, WAITING_FOR_MEANING = range(2)

user_states = {}
with open('abbr.json', 'r', encoding='utf-8') as json_file:
    data_dict = json.load(json_file)


def json_to_txt(j_file, txt_file):
    try:
        with open(j_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(txt_file, 'w', encoding='utf-8') as f:
            for abbr, meaning in data.items():
                f.write(f"{abbr} – {meaning}\n")

    except FileNotFoundError:
        print(f"File not found: {j_file}")
    except json.JSONDecodeError:
        print("Error decoding JSON data.")


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! \n'
                                'Я - бот-Вордбук 🤖\n'
                                '- твой интеллектуальный помощник в распознавании аббревиатур.\n \n'
                                'Помогу быстро найти значения различных сокращений и аббревиатур, используемых в рабочем процессе. \n'
                                'Бот-словарь станет надежным спутником в рабочем процессе, облегчая коммуникацию и повышая эффективность взаимодействия с коллегами и смежными подразделениями💯')
    bot.send_message(m.chat.id, 'Введите аббревиатуру, значение которой хотите узнать👇')


@bot.message_handler(commands=['send_abbr_beautiful'])
def send_abbr_file(message):
    if message.chat.id == 431436587:  # Check if the user is authorized
        f_file = 'abbr.json'
        txt_file = 'abbr.txt'

        json_to_txt(f_file, txt_file)

        with open(txt_file, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="Here is the abbr.txt file.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")


@bot.message_handler(commands=["send_abbr_file"])
def send_abbr_file(m):
    if m.chat.id == 431436587:
        with open('abbr.json', 'rb') as file:
            bot.send_document(m.chat.id, file)
    else:
        bot.send_message(m.chat.id, "Извините, у вас нет доступа к этой команде.")


@bot.message_handler(commands=['new_abbr'])
def new_abbr_command(message):
    if message.chat.id == 431436587:  # Check if the user is authorized
        user_states[message.chat.id] = WAITING_FOR_ABBR
        bot.send_message(message.chat.id, "Пожалуйста, введите аббревиатуру:")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_ABBR)
def receive_abbr(message):
    if message.chat.id == 431436587:  # Check if the user is authorized
        abbr = message.text.strip()
        user_states[message.chat.id] = WAITING_FOR_MEANING  # Set state to waiting for meaning
        user_states[str(message.chat.id) + '_abbr'] = abbr
        bot.send_message(message.chat.id, "Теперь, пожалуйста, введите значение аббревиатуры:")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_MEANING)
def receive_meaning(message):
    if message.chat.id == 431436587:
        meaning = message.text.strip()
        abbr = user_states.get(str(message.chat.id) + '_abbr')
        data_dict[abbr] = meaning

        with open('abbr.json', 'w', encoding='utf-8') as file:
            json.dump(data_dict, file)

        reload_abbrs()

        bot.send_message(message.chat.id, f"Аббревиатура '{abbr}' с значением '{meaning}' успешно добавлена!")

        del user_states[message.chat.id]
        del user_states[str(message.chat.id) + '_abbr']
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")


def reload_abbrs():
    global data_dict
    with open('abbr.json', 'r', encoding='utf-8') as j_file:
        data_dict = json.load(j_file)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() in data_dict.keys():
        bot.send_message(message.from_user.id, data_dict[message.text.lower()])
    else:
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
