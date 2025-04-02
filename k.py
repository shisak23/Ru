import telebot
import random
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7725707594:AAEU7qoiUsMnARZHtEU0hcr_2zbOjgEWDeI"  # Apne bot ka token yahan dalein
OWNER_ID = 7814078698  # Owner ka Telegram User ID
OWNER_USERNAME = "@MRSKYX0"  # Yahan apna Owner Username fix kar do

bot = telebot.TeleBot(TOKEN)

# Approved Users Data (user_id: {"expiry": date, "credits": count})
approved_users = {}

def process_command(message, command_name):
    user_id = message.from_user.id
    
    if user_id not in approved_users:
        bot.reply_to(message, f"❌ Access Denied!\n\n🔹 Contact {OWNER_USERNAME} for access.")
        return

    user_data = approved_users[user_id]
    if user_data["credits"] <= 0:
        bot.reply_to(message, f"❌ You have *0 credits*! Contact {OWNER_USERNAME} to recharge.")
        return

    if datetime.now() > user_data["expiry"]:
        bot.reply_to(message, f"❌ Your access has expired! Contact {OWNER_USERNAME} to renew.")
        return

    approved_users[user_id]["credits"] -= 1

    bot.reply_to(message, f"Send details in format:\n\n`1234567812345678|MM/YY|CVV`", parse_mode="Markdown")

    @bot.message_handler(func=lambda msg: "|" in msg.text)
    def process_details(msg):
        details = msg.text.split("|")
        if len(details) == 3 and len(details[0]) == 16 and len(details[2]) == 3:
            response = random.choice(["✅ Approved", "❌ Declined", "⚠️ Error"])
            bot.reply_to(msg, f"Processing `{command_name}`...\nResult: {response}\n"
                              f"Remaining Credits: {approved_users[user_id]['credits']}")
        else:
            bot.reply_to(msg, "❌ Invalid format! Use `1234567812345678|MM/YY|CVV` format.")

        bot.clear_step_handler_by_chat_id(msg.chat.id)

    bot.register_next_step_handler(message, process_details)

# Custom Keyboard Function
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("🔥 Kill"), KeyboardButton("🔎 Check"))
    keyboard.row(KeyboardButton("📊 My Info"), KeyboardButton("💰 Plans"))
    keyboard.row(KeyboardButton("❓ Help"))
    return keyboard

# /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id in approved_users:
        user_data = approved_users[user_id]
        expiry_date = user_data["expiry"].strftime("%d-%m-%Y")
        credits = user_data["credits"]

        bot.send_message(message.chat.id, f"👋 Welcome!\n"
                                          f"🔹 Your expiry date: {expiry_date}\n"
                                          f"💰 Your credits: {credits}\n"
                                          f"⚡ Use the commands below:", reply_markup=get_main_keyboard())
    else:
        bot.reply_to(message, f"❌ Access Denied!\n\n🔹 Contact {OWNER_USERNAME} for access.")

# Handle Keyboard Buttons
@bot.message_handler(func=lambda message: message.text == "🔥 Kill")
def kill_command(message):
    process_command(message, "KILL")

@bot.message_handler(func=lambda message: message.text == "🔎 Check")
def chk_command(message):
    process_command(message, "CHK")

@bot.message_handler(func=lambda message: message.text == "📊 My Info")
def user_info(message):
    user_id = message.from_user.id
    if user_id not in approved_users:
        bot.reply_to(message, f"❌ You are *not approved*! Contact {OWNER_USERNAME}.")
    else:
        user_data = approved_users[user_id]
        expiry_date = user_data["expiry"].strftime("%d-%m-%Y")
        credits = user_data["credits"]
        
        bot.reply_to(message, f"📊 *Your Account Info:*\n"
                              f"📅 Expiry Date: {expiry_date}\n"
                              f"💰 Remaining Credits: {credits}",
                              parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "💰 Plans")
def show_plans(message):
    plans_text = (
        "🤡 *Bot Plans* 🤫\n\n"
        "💸 *25 credits* - $8 🥇\n"
        "💸 *50 credits* - $15 🎮\n"
        "💸 *100 credits* - $25 😮\n"
        "💵 *200 credits* - $45 🕯🖥\n\n"
        "✅ *Success Rates:*\n"
        "100% Visa Killing ✅\n"
        "70-80% MasterCard Killing 💳"
    )
    bot.reply_to(message, plans_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "❓ Help")
def help_command(message):
    bot.reply_to(message, "📖 *Help Menu:*\n\n"
                          "🔥 *Kill* - Process card\n"
                          "🔎 *Check* - Verify details\n"
                          "📊 *My Info* - Check your account status\n"
                          "💰 *Plans* - View pricing\n"
                          "❓ *Help* - Show help menu",
                          parse_mode="Markdown")

# /approve command (Sirf OWNER use kar sakta hai) - /approve user_id days credits
@bot.message_handler(commands=['approve'])
def approve_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, f"❌ You are not authorized! Contact {OWNER_USERNAME}.")
        return

    try:
        _, user_id, days, credits = message.text.split()
        user_id, days, credits = int(user_id), int(days), int(credits)

        expiry_date = datetime.now() + timedelta(days=days)
        approved_users[user_id] = {"expiry": expiry_date, "credits": credits}

        bot.reply_to(message, f"✅ User `{user_id}` has been approved!\n"
                              f"🔹 Validity: {days} days\n"
                              f"💰 Credits: {credits}",
                              parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "❌ Usage: /approve user_id days credits")

# /setowner command (Sirf OWNER use kar sakta hai) - /setowner new_owner_id
@bot.message_handler(commands=['setowner'])
def set_owner(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, f"❌ You are not authorized! Contact {OWNER_USERNAME}.")
        return

    bot.reply_to(message, "❌ Owner username is fixed and cannot be changed!")

print("Bot is running...")
bot.polling()
