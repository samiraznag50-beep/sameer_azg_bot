import telebot
import os

# Hna k-n-tjib l-Token mn Railway Variables
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hana khdam! Chno bghiti d-dir?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Rk sifti lia: {message.text}")

print("Bot is starting...")
bot.infinity_polling()

