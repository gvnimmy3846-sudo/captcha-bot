from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import random
import string

TOKEN = "8838766761:AAFQRp1bgIiUjCgIaywmDMD_hmRfUO49op8"

captcha_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Captcha Bot Running ✅")

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for member in update.message.new_chat_members:

        captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        captcha_data[member.id] = captcha

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""
Welcome {member.first_name} 👋

Solve this captcha:

{captcha}

Send within 60 seconds.
"""
        )

async def check_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if user_id in captcha_data:

        if text == captcha_data[user_id]:

            await update.message.reply_text("✅ Verified")

            del captcha_data[user_id]

        else:

            await update.message.reply_text("❌ Wrong Captcha")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member)
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, check_captcha)
)

print("Bot Started ✅")

app.run_polling()
