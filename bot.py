import telebot
import time
from requests.exceptions import RequestException
bot = telebot.TeleBot('7060695421:AAGhq8DTppMGjYsf197ZWJAzCA01Iqpydec');

f = open('abbr','r', encoding='UTF-8')
abbrs = f.read().split('\n')
f.close()


@bot.message_handler(commands=["start"])
def start(m,res=False):
   bot.send_message(m.chat.id, 'Привет! \n'
                               'Я - бот-Вордбук 🤖\n'
                               '- твой интеллектуальный помощник в распознавании аббревиатур.\n \n'
                               'Помогу быстро найти значения различных сокращений и аббревиатур, используемых в рабочем процессе. \n'
                               'Бот-словарь станет надежным спутником в рабочем процессе, облегчая коммуникацию и повышая эффективность взаимодействия с коллегами и смежными подразделениями💯')
   bot.send_message(m.chat.id, 'Введите аббревиатуру, значение которой хотите узнать👇')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    countMess = 0
    flag = False
    for abbr in abbrs:
        if flag:
            bot.send_message(message.from_user.id, abbr)
            countMess = 1
            if abbr == '':
                break
        if abbr == message.text.lower():
            flag = True
    if countMess == 0:
        chat_id = 431436587
        bot.send_message(message.from_user.id, 'Я не знаю такой аббревиатуры😞 \n'
                                                   'Но уже отправил Ваш запрос создателю бота для пополнения базы знаний!')
        bot.send_message(chat_id, 'Пользователь пытался найти аббревиатуру: ' + message.text)


bot.polling(none_stop=True, interval=0)

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout = 5)
    except RequestException as err:
        print(err)
        print('* Connection failed, waiting to reconnect...')
        time.sleep(15)
        print('* Reconnecting.')