import telebot
from config_bot import TOKEN, keys
from extensions import Conversation, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # Обрабатываются сообщения, содержащие команды '/start' or '/help'.
def send_start(message):
    text = "Привет! Я помогаю конвертировать валюты. \n Список доступных валют получите по команде /values.\
\n Чтобы начать работу введите: \n <название валюты, цену которой вы хотите узнать> \n <название валюты, \
в которой надо узнать цену первой валюты> \n <количество первой валюты>"
    bot.reply_to(message, text)


@bot.message_handler(commands='values')
def send_values(message):
    text = 'Конвертирую следующие валюты:'
    for k in keys.keys():
        text = '\n'.join((text, k, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types='text')
def convert(message):
    try:
        par = message.text.split(' ')
        if len(par) != 3:
            raise APIException('Введено слишком много(или мало) параметров.\nЧитайте инструкцию')
        base, quote, amount = par
        d = Conversation.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода параметров\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {base} стоит {d} {quote}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)