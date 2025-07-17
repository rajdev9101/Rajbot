# don't remove credit @raj_dev_01
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json, os

TOKEN = "7777252416:AAGnWZmhocENFeVkCRMevEPjvDWg8Z25ecg"
PORT = 8080
WEBHOOK_URL = "https://unable-melisenda-dminemraj-19a84d86.koyeb.app"

# Load log channel
with open("log_channel.json", "r") as f:
    LOG_CHANNEL_ID = int(json.load(f)["log_channel_id"])

# Load filters
FILTERS = {}
if os.path.exists("filters.json"):
    with open("filters.json", "r") as f:
        FILTERS = json.load(f)

# Dummy QA
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
    for k, v in FILTERS.items():
        if k in msg:
            await update.message.reply_text(v)
            return
    for q, a in QA.items():
        if q in msg:
            await update.message.reply_text(a)
            return
    await context.bot.send_message(LOG_CHANNEL_ID, f"New unhandled message:\n{update.message.text}")

def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler("raj", raj_cmd))
    app.add_handler(CommandHandler("filter", set_filter))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    start_bot()
    
