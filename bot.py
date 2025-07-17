# don't remove credit @raj_dev_01
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import json, os, logging

TOKEN = "7777252416:AAGnWZmhocENFeVkCRMevEPjvDWg8Z25ecg"
PORT = 8080

app = Flask(__name__)

# Load log channel
with open("log_channel.json", "r") as f:
    LOG_CHANNEL_ID = int(json.load(f)["log_channel_id"])

# Load filters
if os.path.exists("filters.json"):
    with open("filters.json", "r") as f:
        FILTERS = json.load(f)
else:
    FILTERS = {}

# AI QnA dummy database
QA = {
    "narendra modi": "Narendra Modi is the Prime Minister of India.",
    "raj": "Raj is the creator of this bot. Follow @raj_dev_01 ❤️",
}

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(photo=InputFile("static/start_photo.jpg"),
        caption="👋 Welcome! Type /help to see commands. Powered by @raj_dev_01")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start /help /ping /settings /raj /filter")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive!")

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠 Settings coming soon!")

async def raj_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yeah, I am here — Powered by @raj_dev_01 😎")

async def set_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) >= 2:
        key = context.args[0].lower()
        value = " ".join(context.args[1:])
        FILTERS[key] = value
        with open("filters.json", "w") as f:
            json.dump(FILTERS, f, indent=2)
        await update.message.reply_text(f"✅ Filter added: {key}")
    else:
        await update.message.reply_text("Usage: /filter <keyword> <reply>")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    # Check filters
    for k, v in FILTERS.items():
        if k in msg:
            await update.message.reply_text(v)
            return
    # Check AI-style QnA
    for q, a in QA.items():
        if q in msg:
            await update.message.reply_text(a)
            return

    # Log unhandled messages
    await context.bot.send_message(LOG_CHANNEL_ID, f"New unhandled message:\n{update.message.text}")

# Telegram Bot start
def start_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_cmd))
    app_bot.add_handler(CommandHandler("ping", ping))
    app_bot.add_handler(CommandHandler("settings", settings))
    app_bot.add_handler(CommandHandler("raj", raj_cmd))
    app_bot.add_handler(CommandHandler("filter", set_filter))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    app_bot.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://your-koyeb-app-name.koyeb.app"
    )

@app.route('/')
def home():
    return "Bot Running — @raj_dev_01"

if __name__ == "__main__":
    start_bot()
