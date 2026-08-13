import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot အချက်အလက်များ
TOKEN = "8823017924:AAE2uZqWKlfXw_Pq0kpSF5HCw4uSpKgO7K4"
OWNER_ID = 7936016365  
DEV_CREDIT = "@Obito27891"
SECRET_USERNAME = "obito27891"

bot = telebot.TeleBot(TOKEN)

user_credits = {}
unlimited_users = set()
DEFAULT_FREE_LIMIT = 3

# ယာယီ Leaderboard စာရင်း (Owner ပြင်ဆင်နိုင်ရန်)
leaderboard_data = [
    "1. 🥇 User - 50 Queries",
    "2. 🥈 User - 35 Queries",
    "3. 🥉 User - 20 Queries"
]

# Main Menu (Inline Keyboards)
def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn_scan = InlineKeyboardButton("🔍 Scan", callback_data="btn_scan")
    markup.add(btn_scan)
    
    btn_info = InlineKeyboardButton("👤 Info", callback_data="btn_info")
    btn_leaderboard = InlineKeyboardButton("🏆 Leaderboard", callback_data="btn_leaderboard")
    markup.add(btn_info, btn_leaderboard)
    
    btn_redeem = InlineKeyboardButton("🎁 Redeem", callback_data="btn_redeem")
    btn_find = InlineKeyboardButton("🕵️‍♂️ Find", callback_data="btn_find")
    markup.add(btn_redeem, btn_find)
    
    btn_api = InlineKeyboardButton("🔄 API Status", callback_data="btn_api")
    markup.add(btn_api)
    
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    photo_url = "https://files.catbox.moe/54s39c.jpg" 
    caption_text = (
        "💻 SYSTEM ONLINE\n"
        "──────────────────\n"
        "Choose option below:\n\n"
        f"⚡ Power By {DEV_CREDIT}"
    )
    
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption_text, parse_mode="Markdown", reply_markup=get_main_menu())
    except:
        bot.send_message(message.chat.id, caption_text, parse_mode="Markdown", reply_markup=get_main_menu())

# Inline Button များကို နှိပ်သည့်အခါ
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "btn_scan" or call.data == "btn_find":
        bot.answer_callback_query(call.id, "အချက်အလက်ရှာရန် /info နောက်တွင် ID သို့မဟုတ် Username ထည့်ပါ။")
        bot.send_message(call.message.chat.id, "🔍 ဥပမာ - /info 8746948568 ဟု ရိုက်ထည့်ပါ။", parse_mode="Markdown")
        
    elif call.data == "btn_info":
        credits = "Unlimited (Owner)" if user_id == OWNER_ID or user_id in unlimited_users else user_credits.get(user_id, DEFAULT_FREE_LIMIT)
        bot.answer_callback_query(call.id, f"သင့်ရဲ့ လက်ကျန် Credit: {credits}")
        bot.send_message(call.message.chat.id, f"👤 User Info\n- ID: {user_id}\n- Credits: {credits}\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")
        
    elif call.data == "btn_redeem":
        bot.answer_callback_query(call.id, "Redeem လုပ်ရန် Owner ထံ ဆက်သွယ်ပါ။")
        bot.send_message(call.message.chat.id, f"🎁 Redeem ကုဒ်ဝယ်ယူရန် {DEV_CREDIT} သို့ ဆက်သွယ်ပါ။")
        
    elif call.data == "btn_leaderboard":
        bot.answer_callback_query(call.id, "Leaderboard")
        lb_text = "🏆 Top Users Leaderboard\n──────────────────\n" + "\n".join(leaderboard_data) + f"\n\n⚡ Power By {DEV_CREDIT}"
        bot.send_message(call.message.chat.id, lb_text, parse_mode="Markdown")
        
    elif call.data == "btn_api":
        bot.answer_callback_query(call.id, "Checking API Status...")
        bot.send_message(call.message.chat.id, f"🔄 API Status: ONLINE (Normal)\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")

# Owner က Leaderboard ကို ပြင်ဆင်ရန် Command (ဥပမာ - /setlb 1. 🥇 New User - 100 Queries)
@bot.message_handler(commands=['setlb'])
def set_leaderboard(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ විධාန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ထည့်သွင်းလိုသော Leaderboard စာသားကို ရေးပါ။\nဥပမာ - /setlb 1. 🥇 Name - 100")
        return

    new_line = args[1]
    leaderboard_data.append(new_line)
    bot.reply_to(message, f"✅ Leaderboard သို့ အောင်မြင်စွာ ထည့်သွင်း/ပြင်ဆင်ပြီးပါပြီ။")

# Leaderboard စာရင်းကို အစကနေ ရှင်းလင်းရန် (Owner သာ)
@bot.message_handler(commands=['clearlb'])
def clear_leaderboard(message):
    if message.from_user.id != OWNER_ID:
        return
    leaderboard_data.clear()
    bot.reply_to(message, "✅ Leaderboard စာရင်းများကို ရှင်းလင်းလိုက်ပါပြီ။")

# /info ဖြင့် ရှာဖွေသည့် အဓိက လုပ်ဆောင်ချက်
@bot.message_handler(commands=['info'])
def get_tg_info(message):
    user_id = message.from_user.id
    
    if user_id != OWNER_ID and user_id not in unlimited_users:
        current_credits = user_credits.get(user_id, DEFAULT_FREE_LIMIT)
        if current_credits <= 0:
            no_credit_text = (
                "❌ NO CREDITS\n"
                "──────────────────\n"
                "You have 0 credits. Please redeem a code to continue.\n\n"
                f"⚡ Power By {DEV_CREDIT}"
            )
            bot.reply_to(message, no_credit_text, parse_mode="Markdown")
            return
        user_credits[user_id] = current_credits - 1

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ရှာလိုသည့် ID သို့မဟုတ် Username ထည့်ပါ။\nဥပမာ - /info 8746948568", parse_mode="Markdown")
        return

    query = args[1]
    clean_query = query.replace("@", "").lower()

    sent_msg = bot.reply_to(message, "🔍 အချက်အလက်များကို ရှာဖွေနေပါသည်၊ ခဏစောင့်ပါ...", parse_mode="Markdown")

    api_url = f"https://sbsakib.eu.cc/apis/tg-all-info?key=Demo&tg={query}"

    try:
        response = requests.get(api_url)
        data = response.json()
        
        if isinstance(data, dict) and data.get("success") == False:
            result_text = (
                "⚠️ Result:\n\n"
                "❌ အချက်အလက် ရှာမတွေ့ပါ။ (Data not found across all platforms)\n\n"
                f"⚡ Power By {DEV_CREDIT}"
            )
        else:
            fetched_number = str(data.get("number", ""))
            fetched_id = str(data.get("tg_id", ""))
            
            if clean_query == SECRET_USERNAME or fetched_id == str(OWNER_ID) or fetched_number != "" and fetched_number != "None":
                result_text = (
                    "⚠️ Security Notice:\n\n"
                    "❌ ဤအချက်အလက် (ဖုန်းနံပါတ်/ကိုယ်ရေးအချက်အလက်) ကို ရှာဖွေခွင့်မပြုပါ။ (Protected Profile)\n\n"
                    f"⚡ Power By {DEV_CREDIT}"
                )
            else:
                result_text = f"📊 Result:\n\n`json\n{data}\n```\n\n⚡ Power By {DEV_CREDIT}"
            
        bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode="Markdown")
        
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {e}", chat_id=message.chat.id, message_id=sent_msg.message_id)

# Owner Redeem Command
@bot.message_handler(commands=['redeem'])
def redeem_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ විධාန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "သုံးပုံစံ: `/redeem <User_ID> <1/2/3/u>`", parse_mode="Markdown")
        return

    try:
        target_id = int(args[1])
        amt = args[2].lower()
        if amt == 'u':
            unlimited_users.add(target_id)
            if target_id in user_credits:
                del user_credits[target_id]
        else:
            if target_id in unlimited_users:
                unlimited_users.remove(target_id)
            user_credits[target_id] = int(amt)
            
        bot.reply_to(message, f"✅ User ID: `{target_id}` ကို အောင်မြင်စွာ Redeem လုပ်ပေးလိုက်ပါပြီ။", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Error in arguments.")

print("Bot is running with public leaderboard and owner editing...")
bot.infinity_polling()
