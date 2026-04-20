import telebot
import os
import google.generativeai as genai
import asyncio
import edge_tts

# Configuration
CHOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(CHOT_TOKEN)

# Function bach n-sowbo s-sout (Voiceover)
async def make_voiceover(text, filename):
    # Khtarina sout "Christopher" hit hwa l-wa3er f l-aswat dyal l-AI fabor
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(filename)

@bot.message_handler(commands=['script'])
def handle_script(message):
    topic = message.text.replace('/script', '').strip()
    if not topic:
        bot.reply_to(message, "Sifet smyt l-mawdo3: /script AI for marketing")
        return

    msg = bot.reply_to(message, "🧠 AI is thinking & recording voiceover...")

    try:
        # 1. N-sowbo l-script b Gemini
        prompt = f"Write a 30-second viral TikTok script about {topic}. English only. Focus on professional value."
        response = model.generate_content(prompt)
        script_text = response.text

        # 2. N-rddo l-script sout (MP3)
        audio_file = f"voice_{message.chat.id}.mp3"
        asyncio.run(make_voiceover(script_text, audio_file))

        # 3. N-sifto l-script mktoub
        bot.send_message(message.chat.id, f"📝 **Your Script:**\n\n{script_text}", parse_mode="Markdown")
        
        # 4. N-sifto l-audio
        with open(audio_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio, caption="🔊 Professional Voiceover")
        
        # Mseh l-fichie mlli n-salio bach l-bot ma-i-t3mmerch
        os.remove(audio_file)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"❌ Erreur: {str(e)}")

print("Bot is LIVE with Voiceover ability...")
bot.infinity_polling()
