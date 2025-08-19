import os
import telebot
from telebot import types
import yt_dlp
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# رسالة ترحيب
WELCOME_MSG = (
    "👋 أهلاً بك!\n"
    "أرسل رابط تيك توك، إنستا، يوتيوب أو فيسبوك، وسأرسل لك الفيديو 🎵\n\n"
    "✨ يدعم:\n"
    "• تيك توك: فيديو + صور + MP3\n"
    "• إنستا: ريلز، بوست، ستوري + MP3\n"
    "• يوتيوب وفيسبوك: فيديو MP4"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, WELCOME_MSG)

@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text.strip()
    chat_id = message.chat.id
    bot.send_message(chat_id, "⏳ جاري التحميل، انتظر قليلاً...")

    ydl_opts_video = {
        'format': 'best',
        'outtmpl': 'downloads/video.%(ext)s'
    }

    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        os.makedirs("downloads", exist_ok=True)

        # تنزيل الفيديو
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        # تنزيل الصوت (MP3)
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.extract_info(url, download=True)
            audio_file = "downloads/audio.mp3"

        # إرسال الفيديو
        with open(video_file, 'rb') as vf:
            bot.send_video(chat_id, vf)

        # إرسال الصوت
        with open(audio_file, 'rb') as af:
            bot.send_audio(chat_id, af)

        # تنظيف الملفات المؤقتة
        if os.path.exists(video_file):
            os.remove(video_file)
        if os.path.exists(audio_file):
            os.remove(audio_file)

    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ: {str(e)}")

bot.infinity_polling()