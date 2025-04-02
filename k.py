import telebot
import random

TOKEN = "7725707594:AAEU7qoiUsMnARZHtEU0hcr_2zbOjgEWDeI"  # Apne bot ka token yahan dalein
OWNER_ID = 7814078698  # Owner ka Telegram ID (Find it using @userinfobot)
bot = telebot.TeleBot(TOKEN)

approved_users = ["user1", "user2"]  # Pehle se approved users

def process_command(message, command_name):
    user = message.from_user.username
    if user not in approved_users:
        bot.reply_to(message, f"❌ Access Denied! Buy access: @MRSKYX0)
        return
    
    bot.reply_to(message, f"Send details in format:\n\n`1234567812345678|MM/YY|CVV`", parse_mode="Markdown")

    @bot.message_handler(func=lambda msg: "|" in msg.text)
    def process_details(msg):
        details = msg.text.split("|")
        if len(details) == 3 and len(details[0]) == 16 and len(details[2]) == 3:
            response = random.choice(["✅ Approved", "❌ Declined", "⚠️ Error"])
            bot.reply_to(msg, f"Processing `{command_name}`...\nResult: {response}")
        else:
            bot.reply_to(msg, "❌ Invalid format! Use `1234567812345678|MM/YY|CVV` format.")

        # Remove handler to prevent duplicate responses
        bot.clear_step_handler_by_chat_id(msg.chat.id)

    bot.register_next_step_handler(message, process_details)

# /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user.username
    if user in approved_users:
        welcome_messages = [
            "👋 Welcome to the bot!",
            "🚀 Get ready for action!",
            "🔥 Let's get started!",
            "⚡ Use the commands below:"
        ]
        
        for msg in welcome_messages:
            bot.send_message(message.chat.id, msg)

        bot.send_message(message.chat.id, "✅ Available Commands:\n"
                                          "/kill - Process data\n"
                                          "/chk - Check details\n"
                                          "/help - Get more info")

    else:
        bot.reply_to(message, f"❌ Access Denied! Buy access: @MRSKYX0)

# /kill command
@bot.message_handler(commands=['kill'])
def kill_command(message):
    process_command(message, "KILL")

# /chk command
@bot.message_handler(commands=['chk'])
def chk_command(message):
    process_command(message, "CHK")

# /approve command (Sirf Owner use kar sakta hai)
@bot.message_handler(commands=['approve'])
def approve_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ You are not authorized to approve users!")
        return

    try:
        new_user = message.text.split()[1]  # Username extract karein
        if new_user not in approved_users:
            approved_users.append(new_user)
            bot.reply_to(message, f"✅ User @{new_user} has been approved!")
        else:
            bot.reply_to(message, f"⚠️ User @{new_user} is already approved!")
    except IndexError:
        bot.reply_to(message, "❌ Usage: /approve username")

print("Bot is running...")
bot.polling()
