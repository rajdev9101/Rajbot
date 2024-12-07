from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot Configuration
API_ID = 27084955
API_HASH = "91c88b554ab2a34f8b0c72228f06fc0b"
BOT_TOKEN = "7491549865:AAFQFCm8_UyV7FkfoCSahI_Mw1OC90o9lpY"
LOG_CHANNEL = -1002052558994

# Bot Initialization
bot = Client(
    "PostFinderBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Command: /start
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 **Welcome to Post Finder Bot!**\n\nSearch for posts easily here.\n\n_Powered by @raj_dev21_",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Developer", url="https://t.me/raj_dev21")]]
        )
    )

# Post Search Handler
@bot.on_message(filters.text & ~filters.private)
async def search_posts(client, message):
    search_query = message.text
    try:
        # Search for posts in the log channel
        async for post in bot.search_messages(LOG_CHANNEL, query=search_query):
            await message.reply(
                f"**Post Found:**\n\n{post.text}\n\n_Powered by @raj_dev21_",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("View Post", url=f"https://t.me/c/{str(LOG_CHANNEL)[4:]}/{post.message_id}")]]
                )
            )
    except Exception as e:
        await message.reply("⚠ raj not found for your query. Please try again.")

# Run the Bot
print("🤖 Bot is running...")
bot.run()
# Rajbot
