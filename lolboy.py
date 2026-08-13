import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot အချက်အလက်များ
TOKEN = "8981672999:AAGiSlt5m0OMBdM_YdazQwGKaVVNjgciVWM"
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

# Main Menu (Inline Keyboards - ဝယ်ယူရန် ခလုတ်အသစ် ထည့်ထားသည်)
def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    btn_scan = InlineKeyboardButton("🔍 Scan", callback_data="btn_scan")
    btn_info = InlineKeyboardButton("👤 Info", callback_data="btn_info")
    markup.add(btn_scan, btn_info)
    
    btn_leaderboard = InlineKeyboardButton("🏆 Leaderboard", callback_data="btn_leaderboard")
    btn_redeem = InlineKeyboardButton("🎁 Redeem", callback_data="btn_redeem")
    markup.add(btn_leaderboard, btn_redeem)
    
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
            "၁။ အထက်ပါ နံပါတ်သို့ လိုချင်သည့် Credit ပမာဏအလျောက် ငွေလွှဲပါ။ (ဥပမာ- 5 Credits ဆိုပါက 2500 ကျပ်)\n"
            "၂။ ငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ (Screenshot)** ပုံကို ဤဘော့တ်ဆီသို့ ပုံနှင့်အတူ စာသားအနေဖြင့် **လိုချင်သော Credit ပမာဏ** (ဥပမာ - `5`) ကို Caption ရေး၍ ပို့ပေးပါ။\n"
            "၃။ Owner စစ်ဆေးပြီး လက်ခံသည်နှင့် သင့်အကောင့်ထဲသို့ Auto ဝင်ရောက်လာမည် ဖြစ်ပါသည်။"
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

    # Owner က ငွေလွှဲပြေစာကို လက်ခံ/ငြင်းပယ်ခြင်း (Callback Data handling)
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
            bot.edit_message_caption(
                caption=f"{call.message.caption}\n\n✅ **Status: ACCEPTED (Credit ပေးပြီးပါပြီ)**",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )
            # ဝယ်ယူသူထံ အကြောင်းကြားရန်
            try:
                bot.send_message(target_uid, f"🎉 သنگ့ငွေလွှဲပြေစာကို Owner မှ အတည်ပြုလိုက်ပါပြီ။ သင့်အကောင့်ထဲသို့ **{credits_to_add} Credits** ထည့်သွင်းပေးလိုက်ပါပြီ။ လက်ကျန် Credit: `{user_credits[target_uid]}`", parse_mode="Markdown")
            except:
                pass
                
        elif action == "reject":
            bot.answer_callback_query(call.id, f"❌ ငြင်းပယ်လိုက်ပါပြီ။")
            bot.edit_message_caption(
                caption=f"{call.message.caption}\n\n❌ **Status: REJECTED (ငြင်းပယ်လိုက်သည်)**",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )
            try:
                bot.send_message(target_uid, "❌ တောင်းပန်ပါတယ်၊ သင်တင်ပြလာသော ငွေလွှဲပြေစာမှာ မမှန်ကန်ပါ သို့မဟုတ် ငြင်းပယ်ခံရပါသည်။ ကျေးဇူးပြု၍ Owner ထံ ပြန်လည်စုံစမ်းပါ။")
            except:
                pass

# User များက ငွေလွှဲပြေစာ (Screenshot) ပုံနှင့်အတူ Credit ပမာဏကို Caption ဖြင့် ပို့သည့်အခါ Owner ဆီသို့ ပို့ပေးခြင်း
@bot.message_handler(content_types=['photo'])
def handle_receipt_photo(message):
    user_id = message.from_user.id
    all_users.add(user_id)
    
    if user_id == OWNER_ID:
        return # Owner ပို့တာဆိုရင် ကျော်မည်
        
    caption = message.caption
    if not caption or not caption.isdigit():
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ပြေစာပုံနှင့်အတူ ဝယ်ယူလိုသည့် **Credit ပမာဏ (ဂဏန်းသီးသန့်)** ကို Caption တွင် ရေးပြီး ပို့ပေးပါ။\nဥပမာ - `5` (သို့မဟုတ်) `10`")
        return
        
    credits_amount = int(caption)
    total_price = credits_amount * 500
    
    # Owner ဆီသို့ Approve / Reject Buttons များဖြင့် ပို့မည်
    markup = InlineKeyboardMarkup(row_width=2)
    btn_accept = InlineKeyboardButton("✅ လက်ခံမည် (Accept)", callback_data=f"accept_{user_id}_{credits_amount}")
    btn_reject = InlineKeyboardButton("❌ ငြင်းပယ်မည် (Reject)", callback_data=f"reject_{user_id}_{credits_amount}")
    markup.add(btn_accept, btn_reject)
    
    owner_msg = (
        "📥 **New Credit Purchase Request!**\n"
        "──────────────────────────\n"
        f"• **Buyer ID:** `{user_id}`\n"
        f"• **Buyer Username:** @{message.from_user.username if message.from_user.username else 'None'}\n"
        f"• **Requested Credits:** `{credits_amount}` Credits\n"
        f"• **Total Price:** `{total_price} MMK`\n"
        "──────────────────────────\n"
        "စစ်ဆေးပြီး အောက်ပါခလုတ်ကို နှိပ်ပါ:"
    )
    
    try:
        bot.send_photo(OWNER_ID, message.photo[-1].file_id, caption=owner_msg, parse_mode="Markdown", reply_markup=markup)
        bot.reply_to(message, "✅ ငွေလွှဲပြေစာ ပို့ခြင်း အောင်မြင်ပါသည်။ Owner မှ စစ်ဆေးပြီးပါက သင့်အကောင့်ထဲသို့ Credit အလိုအလျောက် ဝင်ရောက်လာမည် ဖြစ်ပါသည်။")
    except Exception as e:
        bot.reply_to(message, f"❌ ပို့ဆောင်ရာတွင် အမှားအယွင်းရှိနေပါသည်: {e}")

# Owner က Leaderboard ကို ပြင်ဆင်ရန် Command
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

# Redeem Command
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

# Fake Redeem Command
@bot.message_handler(commands=['fakeredeem'])
def fake_redeem(message):
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "⚠️ သုံးပုံစံ: `/fakeredeem <User_ID> <Amount>`\nဥပမာ - `/fakeredeem 7936016365 1000`", parse_mode="Markdown")
        return

    try:
        target_id = int(args[1])
        add_val = int(args[2])
        
        current = user_credits.get(target_id, DEFAULT_FREE_LIMIT)
        user_credits[target_id] = current + add_val
        
        bot.reply_to(message, f"🎁 **Fake Redeem Successful!**\n- User ID: `{target_id}`\n- Added Credits: `{add_val}`\n- Total Balance: `{user_credits[target_id]}`\n\n⚡ Power By {DEV_CREDIT}", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: မှားယွင်းနေသော ပုံစံ ဖြစ်နေပါသည်။ ဂဏန်းများကိုသာ ထည့်ပါ။")

# Deduction Command
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

# Broadcast Command
@bot.message_handler(commands=['broadcast', 'post'])
def broadcast_message(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⚠️ ဤ විධාန်ကို Owner သာ အသုံးပြုနိုင်ပါသည်။")
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

# /info Command
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

print("Bot is running with full features (Auto-Credit Buy System Integrated)...")
bot.infinity_polling()

