from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8838766761:AAFQRp1bgIiUjCgIaywmDMD_hmRfUO49op8"

menu_keyboard = [
    ["Generate Captcha"],
    ["Help"]
]

reply_markup = ReplyKeyboardMarkup(
    menu_keyboard,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome 🔥\nChoose an option:",
        reply_markup=reply_markup
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Generate Captcha":
        await update.message.reply_text(
            "Captcha Generated ✅\n\nCAPTCHA: 583920"
        )

    elif text == "Help":
        await update.message.reply_text(
            "Press Generate Captcha to get captcha."
        )

    else:
        await update.message.reply_text(
            "Choose button from menu."
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

print("Bot running...")
app.run_polling()
