import telebot
import os
import google.generativeai as genai
import asyncio
import edge_tts

# Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# Function bach n-sowbo s-sout
async def make_voiceover(text, filename):
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(filename)

@bot.message_handler(commands=['script'])
def handle_script(message):
    topic = message.text.replace('/script', '').strip()
    if not topic:
        bot.reply_to(message, "Sifet mawdo3: /script AI for business")
        return

    status_msg = bot.reply_to(message, "🧠 Generating script and voiceover...")

    # Jereb l-models b tartib hta wahed i-khdem
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
    script_text = None

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = f"Write a 30-second viral TikTok script about {topic}. English only."
            response = model.generate_content(prompt)
            script_text = response.text
            if script_text:
                break
        except:
            continue

    if not script_text:
        bot.edit_message_text("❌ Model Error. Please check your API Key.", message.chat.id, status_msg.message_id)
        return

    try:
        # Soweb s-sout
        audio_file = f"voice_{message.chat.id}.mp3"
        asyncio.run(make_voiceover(script_text, audio_file))

        # Sifet l-script
        bot.send_message(message.chat.id, f"📝 **Script:**\n\n{script_text}", parse_mode="Markdown")
        
        # Sifet l-audio
        with open(audio_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio, caption="🔊 AI Voiceover")
        
        os.remove(audio_file)
        bot.delete_message(message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"❌ Voice Error: {str(e)}")

print("Bot is ACTIVE with 1.5 Flash Support!")
bot.infinity_polling()
