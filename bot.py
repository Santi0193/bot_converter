import telebot
import config
from extensions import APIException, CurrencyConverter
from telebot.apihelper import ApiTelegramException

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = ("Чтобы использовать этого бота, отправьте сообщение в следующем формате:\n"
                    "<валюта для проверки> <валюта для конвертации> <сумма>\n"
                    "Для просмотра доступных валют воспользуйтесь командой /values")
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(commands=['values'])
def send_values(message):
    values = "Доступные валюты:\nUSD - Доллар США\nEUR - Евро\nRUB - Российский рубль"
    bot.send_message(message.chat.id, values)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            if len(parts) < 3:
                bot.reply_to(message, "Неверный формат сообщения. Недостаточно данных. Пожалуйста, используйте следующий формат: <валюта для проверки> <валюта для конвертации> <сумма>")
            else:
                bot.reply_to(message, "Неверный формат сообщения. Слишком много данных. Пожалуйста, используйте следующий формат: <валюта для проверки> <валюта для конвертации> <сумма>")
            return
        base, quote, amount = parts
        result, base, quote = CurrencyConverter.get_price(base, quote, amount)
        bot.reply_to(message, f"{amount} {base} равно {result} {quote}")
    except ValueError as e:
        words = message.text.split()
        if len(words) == 1:
            bot.reply_to(message, "Неверный формат сообщения. Пожалуйста, используйте следующий формат: <валюта для проверки> <валюта для конвертации> <сумма>")
        elif len(words) == 2:
            bot.reply_to(message, "Неверный формат сообщения. Пожалуйста, укажите сумму.")
        else:
            bot.reply_to(message, f"Неверный формат сообщения. Пожалуйста, проверьте правильность написания валюты для проверки, валюты для конвертации или суммы.")
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
bot.polling()