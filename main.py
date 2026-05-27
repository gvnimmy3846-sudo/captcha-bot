from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8838766761:AAFQRp1bgIiUjCgIaywmDMD_hmRfUO49op8"

async def start(update, context):
    await update.message.reply_text("Bot working!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
