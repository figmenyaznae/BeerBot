import telebot


BOT_TOKEN = '398858338:AAGMhLrE_eNfLwKOfeFQuLhlEH7g878_fOg'
URL = 'https://api.telegram.org/bot%s/' % BOT_TOKEN
MyURL = 'https://fb1488bot.herokuapp.com/'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.reply_to(message, 'Hello, I\'m still in alpha-test mode, please, don\'t speak to me if you are not my developer.')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()