import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# သင့်ရဲ့ Bot Token
BOT_TOKEN = "8783668130:AAHiTdfO8zvsjns1hmiB5ImvjguyK_er7kk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 မင်္ဂလာပါ TikTok Downloader Bot မှ ကြိုဆိုပါတယ်!\n\n"
        "🔗 TikTok ဗီဒီယို လင့်ခ် (Link) ကို ပို့လိုက်ရုံဖြင့် Watermark မပါသော ဗီဒီယိုသန့်သန့်ကို Download လုပ်ပေးပါမည်။"
    )

async def handle_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    # TikTok လင့်ခ် ဟုတ်မဟုတ် စစ်ဆေးခြင်း
    if "tiktok.com" not in url and "vm.tiktok.com" not in url:
        await update.message.reply_text("❌ ကျေးဇူးပြု၍ မှန်ကန်သော TikTok Video Link တစ်ခုသာ ပို့ပေးပါ။")
        return

    status_msg = await update.message.reply_text("📥 TikTok ဗီဒီယိုကို ရယူနေပါပြီ၊ ခဏစောင့်ပါ...")

    try:
        os.makedirs("downloads", exist_ok=True)
        
        # yt-dlp ဖြင့် TikTok ဗီဒီယိုကို Watermark မပါဘဲ ဆွဲရန် Configuration
        ydl_opts = {
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'format': 'best',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        
        await status_msg.edit_text("📤 Telegram သို့ တင်ပေးနေပါပြီ...")
        
        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="✅ **Download Successful!**\n Developer by @lynn_hype_dude"
            )
        
        # ပို့ပြီးပါက ဖုန်း/ဆာဗာထဲမှ ဖိုင်ကို ဖျက်ပစ်ခြင်း (Space ရှင်းရန်)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ ဒေါင်းလုပ်ဆွဲရာတွင် အမှားအယွင်း ရှိနေပါသည်: `{str(e)}`")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_tiktok))

    print("🤖 TikTok Downloader Bot အလုပ်စတင်လုပ်ဆောင်နေပါပြီ...")
    application.run_polling()

if __name__ == '__main__':
    main()

