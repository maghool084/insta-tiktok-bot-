import os
import telebot
from threading import Thread
from flask import Flask

# سيرفر وهمي لإبقاء السيرفر مستيقظاً طوال الوقت
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال بنجاح!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --------------------------------------------------
# ضع توكن بوتك هنا بين العلامتين
BOT_TOKEN = "ضع_التوكن_هنا"
# --------------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "⚡ أهلاً بك! البوت السحابي مستعد للعمل الآن طوال الوقت بدون انقطاع.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # هنا يمكنك إضافة كود معالجة الروابط الخاص بك لاحقاً
    bot.reply_to(message, f"تم استلام رسالتك: {message.text}")

if __name__ == "__main__":
    keep_alive()  # تشغيل السيرفر الوهمي
    print("⚡ البوت السحابي مستعد للعمل على السيرفر...")
    bot.infinity_polling()
