import telebot
import requests
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot အချက်အလက်များ
TOKEN = "8883267652:AAFGJVkbsDxNefl8yOBw-WbPh_3LSg9BQiE"
OWNER_ID = 7936016365  
DEV_CREDIT = "@Obito27891"

bot = telebot.TeleBot(TOKEN)

user_credits = {}
unlimited_users = set()
DEFAULT_FREE_LIMIT = 3

leaderboard_data = [
    "1. 🥇 User - 50 Queries",
    "2. 🥈 User - 35 Queries",
    "3. 🥉 User - 20 Queries"
]

# User ID များကို ဖိုင်ထဲတွင် အမြဲသိမ်းဆည်းရန် Function များ
USER_FILE = "users.txt"

def load_users():
    users = set()
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                try:
                    users.add(int(line.strip()))
                except:
                    pass
    return users

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        with open(USER_FILE, "a") as f:
            f.write(f"{user_id}\n")

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
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Unknown"
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    
    all_users = load_users()
    if user_id not in all_users:
        save_user(user_id)
        if user_id != OWNER_ID:
            start_notify = (
                "🚀 **New User Started Bot!**\n"
                "──────────────────\n"
                f"• Name: {user_name}\n"
                f"• User ID: `{user_id}`\n"
                f"• Username: {username}\n"
                f"• Total Users: `{len(load_users())}`\n"
                "──────────────────"
            )
            try:
                bot.send_message(OWNER_ID, start_notify, parse_mode="Markdown")
            except Exception as e:
                print(f"Error: {e}")
    
    photo_url = "https://files.catbox.moe/54s39c.jpg" 
    caption_text = (
        "👋 **မင်္ဂလာပါ ခင်ဗျာ! Bot မှ ကြိုဆိုပါတယ်။**\n\n"
        "💻 **SYSTEM ONLINE**\n"
        "──────────────────\n"
        "အောက်ပါ Menu များမှ လိုအပ်သည်များကို ရွေးချယ်အသုံးပြုနိုင်ပါသည် -\n\n"
        f"⚡ Power By {DEV_CREDIT}"
    )
    
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption_text, parse_mode="Markdown", reply_markup=get_main_menu())
    except:
        bot.send_message(message.chat.id, caption_text, parse_mode="Markdown", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    save_user(user_id)
    
    if call.data == "btn_scan" or call.data == "btn_find":
        bot.answer_callback_query(call.id, "အချက်အလက်ရှာရန် /info နောက်တွင် ID သို့မဟုတ် Username ထည့်ပါ။")
        bot.send_message(call.message.chat.id, "🔍 ဥပမာ - `/info 8746948568` ဟု ရိုက်ထည့်ပါ။", parse_mode="Markdown")
        
    elif call.data == "btn_info":
        credits = "Unlimited (Owner)" if user_id == OWNER_ID or user_id in unlimited_users else user_credits.get(user_id, DEFAULT_FREE_LIMIT)
        bot.answer_callback_query(call.id, f"သင့်ရဲ့ လက်ကျန် Credit: {credits}")
        bot.send_message(call.message.chat.id, f"👤 **User Info**\n- ID: `{user_id}`\n- Credits: `{credits}`\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")
        
    elif call.data == "btn_redeem":
        bot.answer_callback_query(call.id, "Redeem လုပ်ရန် Owner ထံ ဆက်သွယ်ပါ။")
        bot.send_message(call.message.chat.id, f"🎁 Redeem ကုဒ်ဝယ်ယူရန် {DEV_CREDIT} သို့ ဆက်သွယ်ပါ။")
        
    elif call.data == "btn_leaderboard":
        if user_id != OWNER_ID:
            bot.answer_callback_query(call.id, "⚠️ ဤကဏ္ဍကို Owner သာ ကြည့်ရှုခွင့်ရှိပါသည်။", show_alert=True)
            return
            
        bot.answer_callback_query(call.id, "Owner Leaderboard Panel")
        lb_text = "🏆 **Owner Leaderboard Panel**\n──────────────────\n" + "\n".join(leaderboard_data) + f"\n\n⚡ Power By {DEV_CREDIT}"
        bot.send_message(call.message.chat.id, lb_text, parse_mode="Markdown")
        
    elif call.data == "btn_api":
        bot.answer_callback_query(call.id, "Checking API Status...")
        bot.send_message(call.message.chat.id, f"🔄 **API Status:** `ONLINE` (Normal)\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")

@bot.message_handler(commands=['setlb'])
def set_leaderboard(message):
    if message.from_user.id != OWNER_ID:
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ ဥပမာ - `/setlb 1. 🥇 Name - 100`")
        return
    leaderboard_data.append(args[1])
    bot.reply_to(message, "✅ Leaderboard သို့ အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ။")

@bot.message_handler(commands=['clearlb'])
def clear_leaderboard(message):
    if message.from_user.id != OWNER_ID:
        return
    leaderboard_data.clear()
    bot.reply_to(message, "✅ Leaderboard စာရင်းများ ရှင်းလင်းပြီးပါပြီ။")

@bot.message_handler(commands=['redeem'])
def redeem_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ විධාန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "သုံးပုံစံ: `/redeem <User_ID> <တိုးမည့်ပမာဏ/u>`", parse_mode="Markdown")
        return

    try:
        target_id = int(args[1])
        amt = args[2].lower()
        if amt == 'u':
            unlimited_users.add(target_id)
            if target_id in user_credits:
                del user_credits[target_id]
            bot.reply_to(message, f"✅ User ID: `{target_id}` ကို Unlimited သို့ ပြောင်းလိုက်ပါပြီ။", parse_mode="Markdown")
        else:
            add_val = int(amt)
            current = user_credits.get(target_id, DEFAULT_FREE_LIMIT)
            user_credits[target_id] = current + add_val
            bot.reply_to(message, f"✅ User ID: `{target_id}` သို့ Credit `{add_val}` ထပ်ပေါင်းပေးလိုက်ပါပြီ။ လက်ကျန် Credit အစုစု: `{user_credits[target_id]}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['deduct'])
def deduct_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ විධාန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "သုံးပုံစံ: `/deduct <User_ID> <နုတ်မည့်ပမာဏ (သို့) all>`", parse_mode="Markdown")
        return

    try:
        target_id = int(args[1])
        val = args[2].lower()
        current = user_credits.get(target_id, DEFAULT_FREE_LIMIT)
        
        if val == 'all':
            user_credits[target_id] = 0
            bot.reply_to(message, f"✅ User ID: `{target_id}` ၏ Credit အားလုံးကို 0 သို့ လျှော့ချလိုက်ပါပြီ။", parse_mode="Markdown")
        else:
            sub_val = int(val)
            new_val = max(0, current - sub_val)
            user_credits[target_id] = new_val
            bot.reply_to(message, f"✅ User ID: `{target_id}` ထံမှ Credit `{sub_val}` ကို နုတ်ယူလိုက်ပါပြီ။ ကျန်ရှိ Credit: `{new_val}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['broadcast', 'post'])
def broadcast_message(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ විධාန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    msg_text = message.text.split(maxsplit=1)
    if len(msg_text) < 2:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ပို့လိုသည့် ကြေညာချက်စာသားကို ရေးပါ။\nဥပမာ - `/post မင်္ဂလာပါ ခင်ဗျာ...`")
        return

    content = msg_text[1]
    all_users = load_users()
    success_count = 0
    fail_count = 0

    for uid in all_users:
        try:
            bot.send_message(uid, f"📢 **Announcement:**\n\n{content}\n\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")
            success_count += 1
        except:
            fail_count += 1

    bot.reply_to(message, f"✅ Broadcast / Post ပို့ခြင်း ပြီးပါပြီ။\n- စုစုပေါင်း User: `{len(all_users)}` ဦး\n- အောင်မြင်စွာ ရောက်ရှိသူ: `{success_count}` ဦး\n- မအောင်မြင်သူ (Block/Delete လုပ်ထားသူ): `{fail_count}` ဦး")

@bot.message_handler(commands=['info'])
def get_tg_info(message):
    user_id = message.from_user.id
    save_user(user_id)
    
    if user_id != OWNER_ID and user_id not in unlimited_users:
        current_credits = user_credits.get(user_id, DEFAULT_FREE_LIMIT)
        if current_credits <= 0:
            no_credit_text = (
                "❌ **NO CREDITS**\n"
                "──────────────────\n"
                "You have 0 credits. Please redeem a code to continue.\n\n"
                f"⚡ Power By {DEV_CREDIT}"
            )
            bot.reply_to(message, no_credit_text, parse_mode="Markdown")
            return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ရှာလိုသည့် ID သို့မဟုတ် Username ထည့်ပါ။\nဥပမာ - `/info 8746948568`", parse_mode="Markdown")
        return

    query = args[1]
    sent_msg = bot.reply_to(message, "🔍 **အချက်အလက်များကို ရှာဖွေနေပါသည်၊ ခဏစောင့်ပါ...**", parse_mode="Markdown")

    api_url = f"https://sbsakib.eu.cc/apis/tg-all-info?key=Demo&tg={query}"

    try:
        response = requests.get(api_url, timeout=7)
        
        if response.status_code != 200:
            raise Exception(f"API Server Down (Status: {response.status_code})")
            
        try:
            data = response.json()
        except:
            raise Exception("API returned invalid data format (Not JSON)")
        
        is_empty_result = False
        if isinstance(data, dict):
            if data.get("success") == False or not data or data.get("result") == None:
                is_empty_result = True
            elif all(v is None for v in data.values()):
                is_empty_result = True
        elif not data:
            is_empty_result = True

        if is_empty_result:
            result_text = (
                "⚠️ **Result:**\n\n"
                "❌ အချက်အလက် ရှာမတွေ့ပါ။ (Data not found across all platforms)\n"
                "*(ℹ️ Data မတွေ့ရှိရသဖြင့် သင့် Credit ကို မနှုတ်ယူပါ။)*\n\n"
                f"⚡ Power By {DEV_CREDIT}"
            )
        else:
            if user_id != OWNER_ID and user_id not in unlimited_users:
                current_credits = user_credits.get(user_id, DEFAULT_FREE_LIMIT)
                user_credits[user_id] = current_credits - 1
                
            result_text = f"📊 **Result:**\n\n```json\n{data}\n```\n\n⚡ Power By {DEV_CREDIT}"
            
        bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode="Markdown")
        
    except requests.exceptions.Timeout:
        bot.edit_message_text("❌ **Error:** API ဆာဗာ ချိတ်ဆက်မှု အချိန်ကုန်သွားပါပြီ (Timeout)။ ခဏနေမှ ထပ်ကြိုးစားပါ။\n*(ℹ️ သင့် Credit ကို မနှုတ်ယူပါ။)*", chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode="Markdown")
    except requests.exceptions.ConnectionError:
        bot.edit_message_text("❌ **Error:** API ဆာဗာသို့ ချိတ်ဆက်၍မရပါ (Server Offline / Domain Dead)။\n*(ℹ️ သင့် Credit ကို မနှုတ်ယူပါ။)*", chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode="Markdown")
    except Exception as e:
        bot.edit_message_text(f"❌ **API Error:** ဆာဗာ ချို့ယွင်းနေပါသည်။\n*(ℹ️ သင့် Credit ကို မနှုတ်ယူပါ။)*", chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document', 'video', 'audio', 'sticker'])
def handle_user_messages(message):
    user_id = message.from_user.id
    save_user(user_id)

    if user_id == OWNER_ID:
        if message.reply_to_message:
            replied_msg = message.reply_to_message.text or message.reply_to_message.caption or ""
            try:
                if "User ID:" in replied_msg:
                    lines = replied_msg.split('\n')
                    target_uid = None
                    for line in lines:
                        if "User ID:" in line:
                            target_uid = int(line.split("User ID:")[1].strip())
                            break
                    
                    if target_uid:
                        bot.copy_message(chat_id=target_uid, from_chat_id=message.chat.id, message_id=message.message_id)
                        bot.reply_to(message, "✅ အသုံးပြုသူ (User) ထံသို့ အောင်မြင်စွာ ပို့ပြီးပါပြီ။")
                        return
            except Exception as e:
                print(f"Reply error: {e}")
        return

    if user_id != OWNER_ID:
        user_name = message.from_user.first_name or "Unknown"
        username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
        user_text = message.text or message.caption or "[Media / Attachment]"
        
        formatted_msg = (
            "✉️ **New Message from User!**\n"
            "──────────────────\n"
            f"• Name: {user_name}\n"
            f"• User ID: `{user_id}`\n"
            f"• Username: {username}\n"
            f"• Message: {user_text}\n"
            "──────────────────"
        )
        
        try:
            bot.send_message(OWNER_ID, formatted_msg, parse_mode="Markdown")
            bot.reply_to(message, "💬 သင့်ရဲ့ မက်ဆေ့ခ်ျကို Owner ထံသို့ ပို့ပေးလိုက်ပါပြီ။ ခဏစောင့်ဆိုင်းပေးပါ။")
        except Exception as e:
            print(f"Error sending message to owner: {e}")

print("Bot is running with persistent file-based user storage for broadcasting...")
bot.infinity_polling()

