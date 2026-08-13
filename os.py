import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot Token နှင့် Owner ID
TOKEN = "8970942327:AAEAqj5_1YkxgTFTC36SOr5po6E6ScNahSc"
bot = telebot.TeleBot(TOKEN)
OWNER_ID = 7936016365
OWNER_USERNAME = "@Obito27891"
APK_LINK = "https://t.me/RikeyAndEkaryStore/6035"

# ဒေတာသိမ်းဆည်းရန် နေရာများ
user_data = {}
banned_users = set()
redeem_codes = {"FREE1000": 1000, "VIPBOOST": 500}

def get_user(user_id):
    if user_id == OWNER_ID:
        return {"credit": "Unlimited", "level": "👑 Owner (VVIP+)", "invited": 0}
    
    if user_id not in user_data:
        user_data[user_id] = {
            "credit": 100,  # အစစချင်း 100 စပေးမည်
            "level": "Free User",
            "invited": 0
        }
    return user_data[user_id]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if user_id in banned_users:
        bot.reply_to(message, "❌ ဤ Bot အား အသုံးပြုခွင့် ပိတ်ပင်ခံထားရပါသည်။")
        return
    
    # Referral (Invite) စစ်ဆေးခြင်း
    args = message.text.split()
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            if referrer_id != user_id and user_id not in user_data and referrer_id in user_data:
                if referrer_id != OWNER_ID:
                    user_data[referrer_id]["credit"] += 20
                    user_data[referrer_id]["invited"] += 1
                    bot.send_message(referrer_id, "🎉 သူငယ်ချင်းတစ်ဦးကို ဖိတ်ခေါ်ခြင်းအတွက် Credit +20 ရရှိသွားပါပြီ!")
        except ValueError:
            pass

    user = get_user(user_id)
        
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💰 My Account & Credit", callback_data="my_account"))
    markup.add(InlineKeyboardButton("💳 Credit ဝယ်ယူရန်", url=f"https://t.me/Obtio27891"))
    markup.add(InlineKeyboardButton("👥 🔗 Invite Link ရယူရန်", callback_data="get_invite"))
    markup.add(InlineKeyboardButton("🎁 Redeem Code ထည့်ရန်", callback_data="use_redeem"))
    markup.add(InlineKeyboardButton("🌟 VIP / VVIP ဝယ်ယူရန်", callback_data="buy_vip"))
    markup.add(InlineKeyboardButton("📥 APK Download (1700 Credits)", callback_data="get_apk"))
    
    if user_id == OWNER_ID:
        markup.add(InlineKeyboardButton("👑 Owner Admin Panel", callback_data="owner_panel"))

    text = (
        f"မင်္ဂလာပါ! ဤ Bot တွင် Credit, VIP Level, APK နှင့် Redeem စနစ်များ ပါဝင်ပါသည်။\n\n"
        f"👤 သင့်အဆင့်: {user['level']}\n"
        f"💰 လက်ကျန် Credit: {user['credit']}\n"
        f"👥 ဖိတ်ခေါ်ပြီးသူ: {user['invited']} ယောက်\n\n"
        f"🛒 Credit ထပ်ဝယ်လိုပါက {OWNER_USERNAME} သို့ ဆက်သွယ်နိုင်ပါသည်။"
    )
    bot.reply_to(message, text, reply_markup=markup)

# Owner သီးသန့် Command: /credit user_id amount
@bot.message_handler(commands=['credit'])
def add_credit_command(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ ဤ Command သည် Owner အတွက်သာ ဖြစ်ပါသည်။")
        return
    
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        
        if target_id not in user_data:
            user_data[target_id] = {"credit": 100, "level": "Free User", "invited": 0}
            
        user_data[target_id]["credit"] += amount
        bot.reply_to(message, f"✅ User (`{target_id}`) သို့ Credit `{amount}` အောင်မြင်စွာ ဖြည့်ပေးလိုက်ပါပြီ။ လက်ကျန်: {user_data[target_id]['credit']}")
        bot.send_message(target_id, f"🎉 Owner မှ သင့်ထံသို့ Credit `+{amount}` ထည့်သွင်းပေးလိုက်ပါပြီ!")
    except Exception as e:
        bot.reply_to(message, "❌ ပုံစံ မှားယွင်းနေပါသည်။ ဥပမာ: `/credit 123456789 500` ဟု ရိုက်ပါ။")

# Redeem command စနစ်
@bot.message_handler(commands=['redeem'])
def redeem_command(message):
    user_id = message.from_user.id
    if user_id in banned_users:
        bot.reply_to(message, "❌ ပိတ်ပင်ခံထားရပါသည်။")
        return

    parts = message.text.split()
    
    # Owner မှ Redeem Code အသစ်ဖန်တီးခြင်း: /redeem create CODE AMOUNT
    if len(parts) == 3 and parts[1].lower() == "create":
        if user_id != OWNER_ID:
            bot.reply_to(message, "❌ ဤအမိန့်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
            return
        try:
            code = parts[2]
            amount = int(parts[3])
            redeem_codes[code] = amount
            bot.reply_to(message, f"✅ အောင်မြင်ပါသည်! Redeem Code အသစ်: `{code}` (Credit: {amount}) ကို ဖန်တီးပြီးပါပြီ။")
            return
        except ValueError:
            bot.reply_to(message, "❌ ပုံစံ မှားယွင်းနေပါသည်။ ဥပမာ: `/redeem create PROMO500 500`")
            return

    # ပုံမှန် User များ Redeem Code သုံးခြင်း: /redeem CODENAME
    if len(parts) == 2:
        code = parts[1]
        if code in redeem_codes:
            amount = redeem_codes[code]
            if user_id == OWNER_ID:
                bot.reply_to(message, f"👑 Owner ဖြစ်၍ Credit Unlimited ဖြစ်နေပါသည်။ Code တန်ဖိုး: {amount}")
            else:
                if user_id not in user_data:
                    user_data[user_id] = {"credit": 100, "level": "Free User", "invited": 0}
                user_data[user_id]["credit"] += amount
                bot.reply_to(message, f"🎉 Redeem Code အောင်မြင်ပါသည်! Credit +{amount} ရရှိသွားပါပြီ။ လက်ကျန် Credit: {user_data[user_id]['credit']}")
            del redeem_codes[code]
        else:
            bot.reply_to(message, f"❌ မှားယွင်းနေသော (သို့မဟုတ်) သုံးပြီးသား Redeem Code ဖြစ်ပါသည်။\n🛒 Credit ဝယ်လိုပါက {OWNER_USERNAME} သို့ ဆက်သွယ်ပါ။")
    else:
        bot.reply_to(message, "ℹ️ အသုံးပြုပုံ:\n- Redeem သုံးရန်: `/redeem CODENAME`\n- Code ဖန်တီးရန် (Owner သာ): `/redeem create CODENAME AMOUNT`")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    if user_id in banned_users:
        bot.answer_callback_query(call.id, "❌ ပိတ်ပင်ခံထားရပါသည်။", show_alert=True)
        return

    user = get_user(user_id)

    if call.data == "my_account":
        bot.answer_callback_query(call.id, f"Level: {user['level']} | Credit: {user['credit']} | Invited: {user['invited']}", show_alert=True)

    elif call.data == "get_invite":
        bot_info = bot.get_me()
        bot_username = bot_info.username
        invite_link = f"https://t.me/{bot_username}?start={user_id}"
        
        text = (
            f"🔗 **သင့်ရဲ့ ဖိတ်ခေါ်ရန် (Invite) လင့်ခ်:**\n\n"
            f"`{invite_link}`\n\n"
            f"ℹ️ ဤလင့်ခ်ကို မျှဝေပါက Credit 20 စီ ရရှိမည်ဖြစ်ပါသည်။"
        )
        bot.answer_callback_query(call.id, "Invite link ကို ထုတ်ပေးလိုက်ပါပြီ။")
        bot.send_message(user_id, text, parse_mode="Markdown")

    elif call.data == "use_redeem":
        msg = bot.send_message(user_id, "🎁 Redeem Code သုံးရန် `/redeem CODENAME` ဟု ရိုက်ထည့်ပေးပါ။\n(ဥပမာ: `/redeem FREE1000`)")

    elif call.data == "buy_vip":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🌟 VIP ဝယ်ရန် (50 Credits)", callback_data="upgrade_vip"))
        markup.add(InlineKeyboardButton("💎 VVIP ဝယ်ရန် (100 Credits)", callback_data="upgrade_vvip"))
        markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data="back_home"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🌟 **VIP နှင့် VVIP Level ဝယ်ယူရန်**\n\n- VIP: Credit 50\n- VVIP: Credit 100",
            reply_markup=markup
        )

    elif call.data == "upgrade_vip":
        if user_id == OWNER_ID:
            bot.answer_callback_query(call.id, "👑 Owner ဖြစ်ပြီးသားဖြစ်ပါသည်။", show_alert=True)
            return
            
        if user["credit"] >= 50:
            user["credit"] -= 50
            user["level"] = "🌟 VIP User"
            bot.answer_callback_query(call.id, "🎉 VIP Level သို့ ရောက်ရှိသွားပါပြီ!")
            bot.send_message(user_id, "✅ သတင်းကောင်း! သင်သည် 🌟 VIP User ဖြစ်သွားပါပြီ။")
        else:
            bot.answer_callback_query(call.id, f"❌ Credit မလုံလောက်ပါ။ Credit ဝယ်ယူရန် {OWNER_USERNAME} သို့ ဆက်သွယ်ပါ။", show_alert=True)

    elif call.data == "upgrade_vvip":
        if user_id == OWNER_ID:
            bot.answer_callback_query(call.id, "👑 Owner ဖြစ်ပြီးသားဖြစ်ပါသည်။", show_alert=True)
            return
            
        if user["credit"] >= 100:
            user["credit"] -= 100
            user["level"] = "💎 VVIP User"
            bot.answer_callback_query(call.id, "🎉 VVIP Level သို့ ရောက်ရှိသွားပါပြီ!")
            bot.send_message(user_id, "✅ သတင်းကောင်း! သင်သည် 💎 VVIP User ဖြစ်သွားပါပြီ။")
        else:
            bot.answer_callback_query(call.id, f"❌ Credit မလုံလောက်ပါ။ Credit ဝယ်ယူရန် {OWNER_USERNAME} သို့ ဆက်သွယ်ပါ။", show_alert=True)

    elif call.data == "get_apk":
        if user_id == OWNER_ID or user["level"] in ["🌟 VIP User", "💎 VVIP User", "🛡️ Admin"]:
            bot.answer_callback_query(call.id, "📥 Premium ဖြစ်၍ APK ကို အခမဲ့ ဒေါင်းလုဒ်ဆွဲနိုင်ပါသည်။")
            bot.send_message(user_id, f"📦 သင့်ရဲ့ APK ဖိုင်လင့်ခ်:\n{APK_LINK}")
        else:
            if user["credit"] >= 1700:
                user["credit"] -= 1700
                bot.answer_callback_query(call.id, "APK အတွက် Credit 1700 ဖြတ်လိုက်ပါပြီ။")
                bot.send_message(user_id, f"📦 သင့်ရဲ့ APK ဖိုင်လင့်ခ်:\n{APK_LINK}\n\nကျန်ရှိ Credit: {user['credit']}")
            else:
                bot.answer_callback_query(call.id, f"❌ Credit မလုံလောက်ပါ။ (1700 လိုအပ်သည်)\n🛒 Credit ဝယ်ရန်: {OWNER_USERNAME}", show_alert=True)

    elif call.data == "owner_panel":
        if user_id == OWNER_ID:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📊 Bot Stats (အသုံးပြုသူစာရင်း)", callback_data="bot_stats"))
            markup.add(InlineKeyboardButton("➕ User အား Level ပေးရန်", callback_data="set_user_level"))
            markup.add(InlineKeyboardButton("📢 Broadcast (ကြေညာချက်ပို့ရန်)", callback_data="broadcast_msg"))
            markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data="back_home"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="👑 **Owner Admin Control Panel**\nအောက်ပါ လုပ်ဆောင်ချက်များကို ရွေးချယ်ပါ:\n\n* Redeem Code ဖန်တီးရန် chat ထဲတွင် `/redeem create CODENAME AMOUNT` ဟု ရိုက်နိုင်ပါသည်။",
                reply_markup=markup
            )
        else:
            bot.answer_callback_query(call.id, "❌ ခွင့်ပြုချက်မရှိပါ။", show_alert=True)

    elif call.data == "bot_stats":
        if user_id == OWNER_ID:
            total_users = len(user_data) + 1
            text = f"📊 **Bot Statistics**\n\n- စုစုပေါင်း အသုံးပြုသူ: {total_users} ယောက်\n- ဘန်ထားသူ: {len(banned_users)} ယောက်"
            bot.answer_callback_query(call.id, "Stats ထုတ်ပေးလိုက်ပါပြီ။")
            bot.send_message(user_id, text)

    elif call.data == "set_user_level":
        if user_id == OWNER_ID:
            msg = bot.send_message(user_id, "👤 Level ပေးလိုသော User ID နှင့် Level (ဥပမာ: `12345678 🌟 VIP User`) ကို ရိုက်ထည့်ပေးပါ:")
            bot.register_next_step_handler(msg, process_set_level)

    elif call.data == "broadcast_msg":
        if user_id == OWNER_ID:
            msg = bot.send_message(user_id, "📢 အသုံးပြုသူအားလုံးထံ ပို့လိုသော ကြေညာချက် စာသားကို ရိုက်ထည့်ပါ:")
            bot.register_next_step_handler(msg, process_broadcast)

    elif call.data == "back_home":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(user_id, "ပင်မမီနူးသို့ ပြန်ရောက်ပါပြီ။ /start ကို နှိပ်ပါ။")

def process_set_level(message):
    try:
        parts = message.text.split()
        target_user_id = int(parts[0])
        new_level = " ".join(parts[1:])
        
        if target_user_id not in user_data:
            user_data[target_user_id] = {"credit": 100, "level": "Free User", "invited": 0}
            
        user_data[target_user_id]["level"] = new_level
        bot.send_message(message.from_user.id, f"✅ User {target_user_id} ကို Level `{new_level}` သို့ အောင်မြင်စွာ ပြောင်းလဲပေးလိုက်ပါပြီ။")
        bot.send_message(target_user_id, f"🎉 သင့်အဆင့်ကို Owner မှ `{new_level}` သို့ တိုးမြှင့်ပေးလိုက်ပါပြီ!")
    except Exception as e:
        bot.send_message(message.from_user.id, "❌ ပုံစံ မှားယွင်းနေပါသည်။ ဥပမာ: `12345678 🌟 VIP User` ဟု ရိုက်ပါ။")

def process_broadcast(message):
    text = message.text
    count = 0
    for uid in user_data.keys():
        try:
            bot.send_message(uid, f"📢 **Admin Announcement:**\n\n{text}")
            count += 1
        except Exception:
            pass
    bot.send_message(message.from_user.id, f"✅ ကြေညာချက်ကို အသုံးပြုသူ {count} ယောက်ထံသို့ အောင်မြင်စွာ ပို့ပြီးပါပြီ။")

if __name__ == "__main__":
    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.remove_webhook()
    bot.infinity_polling()

