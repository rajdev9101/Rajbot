from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# Bot Configuration
API_ID = 27084955
API_HASH = "91c88b554ab2a34f8b0c72228f06fc0b"
BOT_TOKEN = "7491549865:AAFQFCm8_UyV7FkfoCSahI_Mw1OC90o9lpY"
LOG_CHANNEL = -1002052558994

# MongoDB Configuration
MONGO_URI = "mongodb+srv://rajdev9101:HH4zVWxX8nwMmAgF@rajdev.1cfcv.mongodb.net/?retryWrites=true&w=majority&appName=Rajdev"  # Update with your MongoDB URI
DB_NAME = "PostFinderDB"

# Initialize MongoDB Client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
user_collection = db["users"]

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
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"
    
    # Save user info to MongoDB
    user_collection.update_one(
        {"user_id": user_id},
        {"$set": {"username": username, "last_seen": message.date}},
        upsert=True
    )
    
    await message.reply(
        "👋 **Welcome to raj Bot!**\n\nSearch for posts easily here.\n\n_Powered by @raj_dev21_",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Developer", url="https://t.me/raj_dev21")]]
        )
    )

# Post Search Handler
@bot.on_message(filters.text & ~filters.private)
async def search_posts(client, message):
    search_query = message.text
    try:
        # Log search query to MongoDB
        user_id = message.from_user.id
        user_collection.update_one(
            {"user_id": user_id},
            {"$push": {"search_queries": {"query": search_query, "timestamp": message.date}}}
        )
        
        # Search for posts in the log channel
        async for post in bot.search_messages(LOG_CHANNEL, query=search_query):
            await message.reply(
                f"**Post Found:**\n\n{post.text}\n\n_Powered by @raj_dev21_",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("View Post", url=f"https://t.me/c/{str(LOG_CHANNEL)[4:]}/{post.message_id}")]]
                )
            )
            break  # Send only the first match
        else:
            await message.reply("⚠ raj No post found for your query. Please try again.")
    except Exception as e:
        await message.reply(f"⚠ Error: {e}")

# Run the Bot
print("🤖 Bot is running...")
bot.run()
