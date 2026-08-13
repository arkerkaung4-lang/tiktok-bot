import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot အချက်အလက်များနှင့် Token အသစ်
TOKEN = "8927090070:AAE8HQFOp7ZIkRV37lF-239E-b_DbZEn23c"
OWNER_ID = 7936016365  
DEV_CREDIT = "@Obito27891"

bot = telebot.TeleBot(TOKEN)

user_credits = {}
unlimited_users = set()
all_users = set()  
DEFAULT_FREE_LIMIT = 3

# ယာယီ Leaderboard စာရင်း
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
    
    btn_buy = InlineKeyboardButton("💳 Buy Credit (1 = 500Ks)", callback_data="btn_buy_menu")
    btn_api = InlineKeyboardButton("🔄 API Status", callback_data="btn_api")
    markup.add(btn_buy, btn_api)
    
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    all_users.add(user_id)
    
    photo_url = "https://files.catbox.moe/54s39c.jpg" 
    caption_text = (
        "💻 **SYSTEM ONLINE**\n"
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
    all_users.add(user_id)
    
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
        
    elif call.data == "btn_buy_menu":
        bot.answer_callback_query(call.id, "Credit ဝယ်ယူရန် နေရာ")
        buy_text = (
            "💳 **Credit ဝယ်ယူရန် (1 Credit = 500 MMK)**\n"
            "──────────────────────────\n"
            "ငွေပေးချေရန် လိပ်စာ/အကောင့်:\n"
            "• **KPay / WavePay:** `09XXXXXXXXX` (အမည် - M...)\n\n"
            "📥 **ဝယ်ယူပုံ အဆင့်ဆင့်:**\n"
            "၁။ ငွေလွှဲပါ။\n"
            "၂။ ပြေစာပုံနှင့် လိုချင်သော Credit ပမာဏ (ဥပမာ - `5`) ကို Caption ရေး၍ ပို့ပါ။"
        )
        bot.send_message(call.message.chat.id, buy_text, parse_mode="Markdown")
        
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

    elif call.data.startswith("accept_") or call.data.startswith("reject_"):
        if user_id != OWNER_ID:
            bot.answer_callback_query(call.id, "⚠️ Owner သာ လုပ်ဆောင်ခွင့်ရှိပါသည်။", show_alert=True)
            return
            
        data_parts = call.data.split("_")
        action = data_parts[0]
        target_uid = int(data_parts[1])
        credits_to_add = int(data_parts[2])
        
        if action == "accept":
            current = user_credits.get(target_uid, DEFAULT_FREE_LIMIT)
            user_credits[target_uid] = current + credits_to_add
            
            bot.answer_callback_query(call.id, f"✅ User ID {target_uid} သို့ {credits_to_add} Credits ထည့်ပေးပြီးပါပြီ။")
            try:
                bot.edit_message_caption(
                    caption=f"{call.message.caption}\n\n✅ **Status: ACCEPTED (Credit ပေးပြီးပါပြီ)**",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    parse_mode="Markdown"
                )
            except:
                pass
            try:
                bot.send_message(target_uid, f"🎉 သင့်ငွေလွှဲပြေစာကို Owner မှ အတည်ပြုလိုက်ပါပြီ။ သင့်အကောင့်ထဲသို့ **{credits_to_add} Credits** ထည့်သွင်းပေးလိုက်ပါပြီ။ လက်ကျန် Credit: `{user_credits[target_uid]}`", parse_mode="Markdown")
            except:
                pass
                
        elif action == "reject":
            bot.answer_callback_query(call.id, f"❌ ငြင်းပယ်လိုက်ပါပြီ။")
            try:
                bot.edit_message_caption(
                    caption=f"{call.message.caption}\n\n❌ **Status: REJECTED (ငြင်းပယ်လိုက်သည်)**",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    parse_mode="Markdown"
                )
            except:
                pass
            try:
                bot.send_message(target_uid, "❌ တောင်းပန်ပါတယ်၊ သင်တင်ပြလာသော ငွေလွှဲပြေစာမှာ မမှန်ကန်ပါ သို့မဟုတ် ငြင်းပယ်ခံရပါသည်။")
            except:
                pass

    elif call.data.startswith("reply_user_"):
        if user_id != OWNER_ID:
            bot.answer_callback_query(call.id, "⚠️ Owner သာ အသုံးပြုနိုင်ပါသည်။", show_alert=True)
            return
            
        target_uid = call.data.split("_")[2]
        bot.answer_callback_query(call.id, f"User ထံ စာပြန်ရန် command ကို အသုံးပြုပါ။")
        bot.send_message(call.message.chat.id, f"💬 ဤ User ထံ စာပြန်ရန် အောက်ပါပုံစံအတိုင်း ရိုက်ထည့်ပါ:\n`/reply {target_uid} <ရေးမည့်စာ>`", parse_mode="Markdown")

# ငွေလွှဲပြေစာပုံ လက်ခံခြင်း
@bot.message_handler(content_types=['photo'])
def handle_receipt_photo(message):
    user_id = message.from_user.id
    all_users.add(user_id)
    
    if user_id == OWNER_ID:
        return 
        
    caption = message.caption
    if not caption or not caption.isdigit():
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ပြေစာပုံနှင့်အတူ ဝယ်ယူလိုသည့် **Credit ပမာဏ (ဂဏန်းသီးသန့်)** ကို Caption တွင် ရေးပြီး ပို့ပေးပါ။")
        return
        
    credits_amount = int(caption)
    total_price = credits_amount * 500
    
    markup = InlineKeyboardMarkup(row_width=2)
    btn_accept = InlineKeyboardButton("✅ လက်ခံမည်", callback_data=f"accept_{user_id}_{credits_amount}")
    btn_reject = InlineKeyboardButton("❌ ငြင်းပယ်မည်", callback_data=f"reject_{user_id}_{credits_amount}")
    btn_reply = InlineKeyboardButton("💬 Reply ပြန်ရန်", callback_data=f"reply_user_{user_id}")
    markup.add(btn_accept, btn_reject)
    markup.add(btn_reply)
    
    owner_msg = (
        "📥 **New Credit Purchase Request!**\n"
        "──────────────────────────\n"
        f"• **Buyer ID:** `{user_id}`\n"
        f"• **Buyer Username:** @{message.from_user.username if message.from_user.username else 'None'}\n"
        f"• **Requested Credits:** `{credits_amount}` Credits\n"
        f"• **Total Price:** `{total_price} MMK`"
    )
    
    try:
        bot.send_photo(OWNER_ID, message.photo[-1].file_id, caption=owner_msg, parse_mode="Markdown", reply_markup=markup)
        bot.reply_to(message, "✅ ငွေလွှဲပြေစာ ပို့ခြင်း အောင်မြင်ပါသည်။ Owner မှ စစ်ဆေးပြီးပါက သင့်အကောင့်ထဲသို့ Credit အလိုအလျောက် ဝင်ရောက်လာမည် ဖြစ်ပါသည်။")
    except Exception as e:
        bot.reply_to(message, f"❌ ပို့ဆောင်ရာတွင် အမှားအယွင်းရှိနေပါသည်: {e}")

# Owner က User ထံ တိုက်ရိုက် စာပြန်ရန် Command (/reply <user_id> <message>)
@bot.message_handler(commands=['reply'])
def owner_reply_user(message):
    if message.from_user.id != OWNER_ID:
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        bot.reply_to(message, "⚠️ အသုံးစံနှုန်း: `/reply <User_ID> <ရေးမည့်စာ>`", parse_mode="Markdown")
        return

    try:
        target_id = int(args[1])
        reply_msg = args[2]
        
        bot.send_message(target_id, f"💬 **Admin / Owner မှ ပြောကြားချက်:**\n\n{reply_msg}\n\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")
        bot.reply_to(message, f"✅ User ID: `{target_id}` ထံသို့ စာ အောင်မြင်စွာ ပို့ပြီးပါပြီ။", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# Owner က Leaderboard ချိန်ညှိရန် Commands
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

# 1. Redeem Command: Owner က /redeem <User_ID> <Amount / u> ဖြင့် တိုက်ရိုက်ထည့်ပေးရန် (u = Unlimited)
@bot.message_handler(commands=['redeem'])
def redeem_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ ဝိဓာန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "သုံးပုံစံ: `/redeem <User_ID> <တိုးမည့်ပမာဏ (သို့) u>`\n(ဥပမာ - `/redeem 123456789 5` သို့မဟုတ် `/redeem 123456789 u`)", parse_mode="Markdown")
        return

    try:
        target_id = int(args[1])
        amt = args[2].lower()
        if amt == 'u':
            unlimited_users.add(target_id)
            if target_id in user_credits:
                del user_credits[target_id]
            bot.reply_to(message, f"✅ User ID: `{target_id}` ကို **Unlimited** သို့ ပြောင်းလိုက်ပါပြီ။", parse_mode="Markdown")
            try:
                bot.send_message(target_id, f"🎉 Owner မှ သင့်အကောင့်အား **Unlimited** သို့ ပြောင်းလဲပေးလိုက်ပါပြီ။", parse_mode="Markdown")
            except:
                pass
        else:
            add_val = int(amt)
            current = user_credits.get(target_id, DEFAULT_FREE_LIMIT)
            user_credits[target_id] = current + add_val  
            bot.reply_to(message, f"✅ User ID: `{target_id}` သို့ Credit `{add_val}` ထပ်ပေါင်းပေးလိုက်ပါပြီ။ လက်ကျန် Credit အစုစု: `{user_credits[target_id]}`", parse_mode="Markdown")
            try:
                bot.send_message(target_id, f"🎉 သင့်အကောင့်ထဲသို့ Credit `+{add_val}` ထည့်သွင်းပေးလိုက်ပါပြီ။ လက်ကျန် Credit: `{user_credits[target_id]}`", parse_mode="Markdown")
            except:
                pass
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# 2. Deduction Command: Credit ကို အကုန် (သို့မဟုတ် လိုသလောက်) နုတ်ယူရန် (-=)
@bot.message_handler(commands=['deduct'])
def deduct_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ ဝိဓာန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "သုံးပုံစံ: `/deduct <User_ID> <နုတ်မည့်ပမာဏ (သို့) all>`", parse_mode="Markdown")
        return

    try:
        target_id = int(args[1])
        val = args[2].lower()
        
        # အကယ်၍ user က unlimited ဖြစ်နေရင် unlimited စာရင်းထဲကပါ ဖြုတ်ထုတ်မည်
        if target_id in unlimited_users and val != 'all':
            unlimited_users.remove(target_id)
            user_credits[target_id] = DEFAULT_FREE_LIMIT

        current = user_credits.get(target_id, DEFAULT_FREE_LIMIT)
        
        if val == 'all':
            if target_id in unlimited_users:
                unlimited_users.remove(target_id)
            user_credits[target_id] = 0
            bot.reply_to(message, f"✅ User ID: `{target_id}` ၏ Credit အားလုံးကို 0 သို့ လျှော့ချလိုက်ပါပြီ။", parse_mode="Markdown")
        else:
            sub_val = int(val)
            new_val = max(0, current - sub_val)
            user_credits[target_id] = new_val
            bot.reply_to(message, f"✅ User ID: `{target_id}` ထံမှ Credit `{sub_val}` ကို နုတ်ယူလိုက်ပါပြီ။ ကျန်ရှိ Credit: `{new_val}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# 3. Broadcast Post Command: /start နှိပ်ထားသူ အားလုံးထံသို့ ပို့ရန် (Owner သာ)
@bot.message_handler(commands=['broadcast', 'post'])
def broadcast_message(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ ဝိဓာန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
        return

    msg_text = message.text.split(maxsplit=1)
    if len(msg_text) < 2:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ပို့လိုသည့် စာသားကို ရေးပါ။\nဥပမာ - `/post မင်္ဂလာပါ ခင်ဗျာ...`")
        return

    content = msg_text[1]
    success_count = 0
    fail_count = 0

    for uid in all_users:
        try:
            bot.send_message(uid, f"📢 **Announcement:**\n\n{content}\n\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")
            success_count += 1
        except:
            fail_count += 1

    bot.reply_to(message, f"✅ Broadcast ပြီးပါပြီ။\n- ပို့နိုင်သူ: `{success_count}` ဦး\n- မအောင်မြင်သူ: `{fail_count}` ဦး")

# /info ဖြင့် ရှာဖွေသည့် အဓိက လုပ်ဆောင်ချက်
@bot.message_handler(commands=['info'])
def get_tg_info(message):
    user_id = message.from_user.id
    all_users.add(user_id)
    
    if user_id != OWNER_ID and user_id not in unlimited_users:
        current_credits = user_credits.get(user_id, DEFAULT_FREE_LIMIT)
        if current_credits <= 0:
            no_credit_text = (
                "❌ **NO CREDITS**\n"
                "──────────────────\n"
                "You have 0 credits. Please buy credits to continue.\n\n"
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
        response = requests.get(api_url)
        data = response.json()
        
        if isinstance(data, dict) and data.get("success") == False:
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
        
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {e}", chat_id=message.chat.id, message_id=sent_msg.message_id)

# User များ ပို့သမျှ စာသားများကို ဖမ်းယူပြီး Owner ဆီသို့ ပို့ပေးခြင်း
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_messages(message):
    user_id = message.from_user.id
    all_users.add(user_id)
    
    if user_id == OWNER_ID:
        return

    user_text = message.text
    user_name = message.from_user.first_name if message.from_user.first_name else "Unknown"
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"

    markup = InlineKeyboardMarkup()
    btn_reply = InlineKeyboardButton("💬 Reply ပြန်ရန်", callback_data=f"reply_user_{user_id}")
    markup.add(btn_reply)

    forward_msg = (
        "📩 **New Message from User!**\n"
        "──────────────────────────\n"
        f"• **Name:** {user_name}\n"
        f"• **User ID:** `{user_id}`\n"
        f"• **Username:** {username}\n"
        f"• **Message:** {user_text}\n"
        "──────────────────────────"
    )
    
    try:
        bot.send_message(OWNER_ID, forward_msg, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(f"Error sending message to owner: {e}")

    reply_text = (
        f"📩 သင်၏ မက်ဆေ့ဂျ်ကို Owner ထံသို့ ပို့ပြီးပါပြီ။\n"
        f"အမြန်ဆုံး အကြောင်းပြန်ပေးပါမည်။ ကျေးဇူးတင်ပါသည်။\n\n"
        f"⚡ Power By {DEV_CREDIT}"
    )
    bot.reply_to(message, reply_text, parse_mode="Markdown")

print("Bot is running with full features and redeem command set to (id amount/u)...")
bot.infinity_polling()
