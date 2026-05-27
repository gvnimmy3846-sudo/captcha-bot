from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random
import string
import json

TOKEN = "8838766761:AAFQRp1bgIiUjCgIaywmDMD_hmRfUO49op8"

ADMIN_ID = 1282253529

USERS_FILE = "users.json"
WITHDRAW_FILE = "withdrawals.json"

captchas = {}
withdraw_mode = {}

def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except:
        return {}

def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file)

users = load_data(USERS_FILE)
withdrawals = load_data(WITHDRAW_FILE)

def generate_captcha():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

keyboard = [
    ["🔄 Next Captcha"],
    ["💰 Balance", "🏧 Withdraw"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

async def send_captcha(update, user_id):

    captcha = generate_captcha()
    captchas[user_id] = captcha

    await update.message.reply_text(
        f"🧩 Solve this captcha:\n\n{captcha}",
        reply_markup=reply_markup
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)
    username = update.effective_user.username

    if user_id not in users:

        users[user_id] = {
            "username": username,
            "balance": 0,
            "solved": 0
        }

        save_data(USERS_FILE, users)

    await update.message.reply_text(
        "✅ Welcome To Captcha Earn Bot"
    )

    await send_captcha(update, user_id)

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)
    text = update.message.text

    if user_id not in users:
        return

    if text == "💰 Balance":

        await update.message.reply_text(
            f"💰 Balance: ₹{users[user_id]['balance']:.2f}\n"
            f"📌 Solved: {users[user_id]['solved']}"
        )

    elif text == "🔄 Next Captcha":

        await send_captcha(update, user_id)

    elif text == "🏧 Withdraw":

        if users[user_id]["balance"] >= 10:

            withdraw_mode[user_id] = True

            await update.message.reply_text(
                "Send Your UPI ID"
            )

        else:

            await update.message.reply_text(
                "❌ Minimum ₹10 Required"
            )

    elif user_id in withdraw_mode:

        upi = text

        withdrawal_id = str(len(withdrawals) + 1)

        withdrawals[withdrawal_id] = {
            "user_id": user_id,
            "username": users[user_id]["username"],
            "upi": upi,
            "amount": users[user_id]["balance"],
            "status": "Pending"
        }

        save_data(WITHDRAW_FILE, withdrawals)

        withdraw_mode.pop(user_id)

        await update.message.reply_text(
            "✅ Withdrawal Request Submitted"
        )

    elif user_id in captchas:

        if text == captchas[user_id]:

            users[user_id]["balance"] += 0.05
            users[user_id]["solved"] += 1

            save_data(USERS_FILE, users)

            await update.message.reply_text(
                f"✅ Correct!\n\n"
                f"💰 Balance: ₹{users[user_id]['balance']:.2f}\n"
                f"📌 Solved: {users[user_id]['solved']}"
            )

            await send_captcha(update, user_id)

        else:

            await update.message.reply_text(
                "❌ Wrong Captcha"
            )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id == ADMIN_ID:

        total_users = len(users)

        msg = f"👨‍💼 ADMIN PANEL\n\n👥 Total Users: {total_users}\n\n"

        for uid, data in users.items():

            msg += (
                f"🆔 {uid}\n"
                f"👤 {data['username']}\n"
                f"💰 ₹{data['balance']:.2f}\n"
                f"📌 Solved: {data['solved']}\n\n"
            )

        await update.message.reply_text(msg)

    else:

        await update.message.reply_text(
            "❌ Access Denied"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

app.run_polling()
