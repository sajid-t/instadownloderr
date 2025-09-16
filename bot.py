import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = "8463417691:AAGjI8dX5Sw_xoxHVpQbJK_uOZv1Id9qa_U"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Hello! Mujhe Instagram reel ka link bhejo, main video bhej dunga.""")

async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        await update.message.reply_text("""Ye valid Instagram link nahi hai.""")
        return
    await update.message.reply_text("""⏳ Download ho raha hai...""")
    ydl_opts = {'outtmpl': os.path.join(tempfile.gettempdir(), 'reel.%(ext)s'), 'format': 'mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        with open(file_path, 'rb') as f:
            await update.message.reply_video(f)
        os.remove(file_path)
        await update.message.reply_text("""✅ Done! Video bhej diya.""")
    except Exception as e:
        await update.message.reply_text(f"""⚠️ Error: {str(e)}""")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_reel))
    print("🤖 Bot started polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
