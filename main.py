from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import string

# =========================
# BOT TOKEN
# =========================
TOKEN = "8838766761:AAFQRp1bgIiUjCgIaywmDMD_hmRfUO49op8"

#Store captcha answers
captcha_data = {}

# =========================
# START COMMAND
# =========================
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Captcha Bot Working ✅")

# =========================
# NEW MEMBER JOIN
# =========================
def new_member(update: Update, context: CallbackContext):

    for member in update.message.new_chat_members:

        # Generate random captcha
        captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # Save captcha
        captcha_data[member.id] = captcha

        # Send captcha
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""
Welcome {member.first_name} 👋

Solve this captcha to stay in group:

➡️ {captcha}

Send the captcha in chat within 60 seconds.
"""
        )

        # Kick after 60 sec if wrong
        context.job_queue.run_once(
            kick_user,
            60,
            context={
                "chat_id": update.effective_chat.id,
                "user_id": member.id
            }
        )

# =========================
# CHECK CAPTCHA
# =========================
def check_captcha(update: Update, context: CallbackContext):

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if user_id in captcha_data:

        correct = captcha_data[user_id]

        if text == correct:

            update.message.reply_text("✅ Verification Successful")

            del captcha_data[user_id]

        else:

            update.message.reply_text("❌ Wrong Captcha")

# =========================
# KICK USER
# =========================
def kick_user(context: CallbackContext):

    job = context.job.context

    chat_id = job["chat_id"]
    user_id = job["user_id"]

    if user_id in captcha_data:

        try:
            context.bot.kick_chat_member(chat_id, user_id)

            context.bot.send_message(
                chat_id=chat_id,
                text=f"❌ User removed for wrong captcha"
            )

            del captcha_data[user_id]

        except:
            pass

# =========================
# MAIN
# =========================
updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

# Commands
dp.add_handler(CommandHandler("start", start))

# New members
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

# Captcha answers
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_captcha))

print("Captcha Bot Started ✅")

updater.start_polling()
updater.idle()

