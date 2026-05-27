import random
import string
from io import BytesIO

from PIL import Image, ImageDraw
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

TOKEN = "8838766761:AAFQRp1bgIiUjCgIaywmDMD_hmRfUO49op8"

users = {}

# ---------------- CAPTCHA ---------------- #

def generate_captcha():
    chars = string.ascii_uppercase + string.digits
    text = ''.join(random.choices(chars, k=6))

    image = Image.new('RGB', (250, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    draw.text((50, 30), text, fill=(0, 0, 0))

    bio = BytesIO()
    bio.name = "captcha.png"

    image.save(bio, "PNG")
    bio.seek(0)

    return text, bio

# ---------------- BUTTONS ---------------- #

def buttons():
    keyboard = [
        [
            InlineKeyboardButton("💳 Balance", callback_data="balance"),
            InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

# ---------------- SEND CAPTCHA ---------------- #

async def send_captcha(update, context):

    user_id = update.effective_user.id

    captcha_text, captcha_image = generate_captcha()

    users[user_id]["captcha"] = captcha_text

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=captcha_image,
        caption="🔐 Solve this 6-digit captcha",
        reply_markup=buttons()
    )

# ---------------- START ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {
            "balance": 0.0,
            "captcha": ""
        }

    await send_captcha(update, context)

# ---------------- REPLY ---------------- #

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in users:
        await update.message.reply_text("Send /start first")
        return

    answer = update.message.text.upper()

    correct = users[user_id]["captcha"]

    if answer == correct:

        users[user_id]["balance"] += 0.05

        balance = round(users[user_id]["balance"], 2)

        await update.message.reply_text(
            f"✅ Correct\n\n"
            f"💰 +0.05 Added\n"
            f"💳 Balance: {balance}"
        )

        await send_captcha(update, context)

    else:

        await update.message.reply_text("❌ Wrong captcha")

# ---------------- BUTTON ACTIONS ---------------- #

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in users:
        return

    if query.data == "balance":

        balance = round(users[user_id]["balance"], 2)

        await query.message.reply_text(
            f"💳 Your Balance: {balance}"
        )

    elif query.data == "withdraw":

        balance = users[user_id]["balance"]

        if balance < 1:
            await query.message.reply_text(
                "❌ Minimum withdraw is 1"
            )
        else:
            await query.message.reply_text(
                "✅ Withdraw request submitted"
            )

# ---------------- MAIN ---------------- #

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
)

app.add_handler(CallbackQueryHandler(button_click))

print("Bot Running...")

app.run_polling()
