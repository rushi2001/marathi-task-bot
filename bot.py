from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import json

DATA_FILE = 'users.json'

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    uid = str(user.id)

    args = context.args
    ref_by = args[0] if args else None

    if uid not in users:
        users[uid] = {
            "name": user.first_name,
            "ref_by": ref_by,
            "points": 0,
            "team": [],
            "task_done": []
        }
        if ref_by and ref_by in users:
            users[ref_by]["team"].append(uid)
        save_users()

    bot_msg = f"""👋 नमस्कार *{user.first_name}*!
तुमचं स्वागत आहे "Task करा आणि पैसे कमवा 💰" बोटमध्ये.

📲 तुमचा रेफरल कोड: `{uid}`
🔗 लिंक: https://t.me/{context.bot.username}?start={uid}

🎯 टास्क साठी वापरा: /task
💰 बॅलन्स बघण्यासाठी: /balance
👥 माझी टीम: /team
"""
    update.message.reply_text(bot_msg, parse_mode='Markdown')

def main():
    TOKEN = os.getenv("7860435614:AAEOSjPPlxSr2jMXHQ7hvhJd7WFHiNvL4sI")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
