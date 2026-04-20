import telebot
import os
import google.generativeai as genai

# Configuration
CHOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(CHOT_TOKEN)

@bot.message_handler(commands=['script'])
def make_script(message):
    topic = message.text.replace('/script', '').strip()
    if not topic:
        bot.reply_to(message, "Sifet lia smyt l-AI tool aw l-fikra. Mital: /script Canva AI")
        return

    bot.reply_to(message, "Generating script for the US audience... 🇺🇸")
    
    prompt = f"""
    Write a viral 30-second TikTok/Reel script about {topic}. 
    Target Audience: USA Professionals & Creators.
    Language: Engaging English.
    Structure:
    1. Hook (Capture attention in 3s)
    2. The Value (What does the tool do?)
    3. Call to action.
    Also, provide 5 high-ranking hashtags.
    """
    
    response = model.generate_content(prompt)
    bot.reply_to(message, response.text)

print("Bot is starting with Gemini Brain...")
bot.infinity_polling()
