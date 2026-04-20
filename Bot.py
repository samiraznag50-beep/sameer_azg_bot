import telebot
import os

# Had l-token ghadi n-zidouh f Railway men ba3d
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salam! l-bot dyalk khdam f Railway 🚀")

bot.infinity_polling()
