from telegram.ext import Updater, CommandHandler

TOKEN = "8838766761:AAFQRp1bgIiUjCgIaywmDMD_hmRfUO49op8"

def start(update, context):
    update.message.reply_text("Bot working successfully ✅")

updater = Updater(TOKEN)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))

print("Bot Started...")

updater.start_polling()
updater.idle()
