import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# ပေးထားသော Bot Token
BOT_TOKEN = "8783668130:AAHiTdfO8zvsjns1hmiB5ImvjguyK_er7kk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 မင်္ဂလာပါ!\n\n"
        "ဤ Bot သည် Direct Link များ၊ YouTube သို့မဟုတ် Website လင့်ခ်များကို ပို့လိုက်ရုံဖြင့် ဖိုင်များကို Download ဆွဲပြီး Telegram သို့ တင်ပေးမည့် Bot ဖြစ်ပါသည်။\n\n"
        "လင့်ခ်တစ်ခုကို ပို့ပြီး စမ်းကြည့်ပါ။"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not url.startswith("http"):
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ မှန်ကန်သော Link တစ်ခု ပို့ပေးပါ။")
        return

    status_msg = await update.message.reply_text("📥 လင့်ခ်ကို စစ်ဆေးနေပါပြီ၊ ခဏစောင့်ပါ...")

    try:
        os.makedirs("downloads", exist_ok=True)
        
        # YouTube သို့မဟုတ် Supported Links များအတွက် yt-dlp သုံးခြင်း
        if any(domain in url for domain in ["youtube.com", "youtu.be", "instagram.com", "facebook.com", "tiktok.com"]):
            await status_msg.edit_text("🔄 ဗီဒီယိုကို Download ဆွဲနေပါပြီ...")
            
            ydl_opts = {
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'format': 'best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
            
            await status_msg.edit_text("📤 Telegram သို့ တင်ပေးနေပါပြီ...")
            with open(file_path, 'rb') as video_file:
                await update.message.reply_video(video=video_file)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
        else:
            # Direct File Download (Zip, Apk, Images, PDF etc.)
            await status_msg.edit_text("📥 ဖိုင်ကို Download ဆွဲနေပါပြီ...")
            
            response = requests.get(url, stream=True)
            file_name = url.split("/")[-1].split("?")[0]
            if not file_name or "." not in file_name:
                file_name = "downloaded_file.zip"
                
            file_path = os.path.join("downloads", file_name)
            
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            
            await status_msg.edit_text("📤 Telegram သို့ တင်ပေးနေပါပြီ...")
            with open(file_path, 'rb') as doc_file:
                await update.message.reply_document(document=doc_file)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ အမှားအယွင်း ဖြစ်ပေါ်သွားသည်: `{str(e)}`")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Bot အလုပ်စတင်လုပ်ဆောင်နေပါပြီ...")
    application.run_polling()

if __name__ == '__main__':
    main()

