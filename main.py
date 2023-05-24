import telebot
from config import TOKEN, keys
from extensions import ConvertException, WalletConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Приветствую!' \
           ' Чтобы начать работу, введите команду боту в следующем формате:' \
           ' <имя валюты>' \
           ' <в какую валюту перевести>' \
           ' <количество переводимой валюты> \n' \
           'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    value = message.text.split(' ')
    try:
        if len(value) != 3:
            raise ConvertException('Некорректно введены параметры ')
        answer = WalletConverter.get_price(*value)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка ввода данных. {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()
