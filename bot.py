import os
import time
import telebot
import yt_dlp

# جلب التوكن بشكل آمن وسري من إعدادات السيرفر السحابي
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ خطأ: لم يتم العثور على التوكن! تأكد من إضافته في إعدادات السيرفر السحابي (Render).")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# دالة تحميل ذكية ومخصصة للسيرفر (تدعم السرعة والتوافق التام)
def download_video(url, chat_id):
    file_name = f"video_{chat_id}_{int(time.time())}"
    
    ydl_opts = {
        # جلب جودة متوسطة سريعة ومدمجة تلقائياً لضمان السرعة والتوافق على السيرفر
        'format': 'best[height<=720][ext=mp4]/best', 
        'outtmpl': f'{file_name}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

# استقبال أمر البدء /start (كلام ترحيبي حلو ومرتب)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"✨ أهلاً وسهلاً بك يا غالي {user_name} في بوتك المفضّل! ✨\n\n"
        "نورت البوت، أنا هنا لخدمتك ومساعدتك في حفظ مقاطعك المفضلة بلمح البصر وبأعلى سرعة ممكنة. 🚀🎬\n\n"
        "كل ما عليك فعله هو إرسال رابط المقطع من:\n"
        "📸 إنستغرام (Instagram Reels & Videos)\n"
        "🎵 تيك توك (TikTok Videos)\n\n"
        "أرسل الرابط الآن وانتظر سحري الخاص! ✨\n\n"
        "──────────────────\n"
        "👑 المطور الحصري للبوت: @Maghol084"
    )
    bot.reply_to(message, welcome_text)

# معالجة الروابط المرسلة
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    chat_id = message.chat.id
    
    # فحص الرابط (إنستغرام وتيك توك فقط، وحذف الفيسبوك بناءً على طلبك)
    if any(platform in url.lower() for platform in ['tiktok.com', 'instagram.com']):
        msg = bot.reply_to(message, "⏳ جاري جلب المقطع ومعالجته يا غالي، ثواني ويكون عندك...")
        
        try:
            # بدء التحميل
            video_file = download_video(url, chat_id)
            
            # إرسال الفيديو للمستخدم
            with open(video_file, 'rb') as video:
                bot.send_video(chat_id, video, reply_to_message_id=message.message_id, timeout=60)
            
            # تنظيف وحذف الملف المؤقت والرسالة السابقة لترتيب الشات
            bot.delete_message(chat_id, msg.message_id)
            if os.path.exists(video_file):
                os.remove(video_file)
                
        except Exception as e:
            error_msg = str(e)
            # تنبيه ذكي إذا حاول المستخدم رفع صورة أو ألبوم بدلاً من فيديو
            if "unsupported url" in error_msg.lower() or "photo" in url.lower():
                bot.edit_message_text("⚠️ عذراً يا غالي، البوت مخصص لتحميل مقاطع الفيديو فقط، ولا يدعم الصور أو الألبومات المجمعة حالياً.", chat_id, msg.message_id)
            else:
                bot.edit_message_text(f"❌ عذراً يا غالي، حدث خطأ أثناء التحميل.\nتأكد أن الحساب عام وليس خاصاً.\n\nإذا استمرت المشكلة، تواصل مع مطوري الغالي هنا: @Maghol084", chat_id, msg.message_id)
            
            if 'video_file' in locals() and os.path.exists(video_file):
                os.remove(video_file)
    else:
        bot.reply_to(message, "⚠️ يا غالي هذا الرابط غير مدعوم!\nالبوت مخصص لتحميل مقاطع (تيك توك وإنستغرام) فقط. 🖤\n\nلأي استفسار تواصل مع المطور: @Maghol084")

# تشغيل البوت
print("⚡ البوت السحابي مستعد للعمل على السيرفر...")
bot.infinity_polling()
