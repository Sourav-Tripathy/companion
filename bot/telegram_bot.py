from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from utils.config import TELEGRAM_BOT_TOKEN
from utils.db import db
from models.mood_entry import MoodEntry
from models.user import User
from services.question_service import get_next_question

# Define the mood options
MOOD_OPTIONS = [['😊', '🙂', '😐'], ['😞', '😠', '😰']]
MOOD_KEYBOARD = ReplyKeyboardMarkup(MOOD_OPTIONS, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_info = update.effective_user
    user = await db.users.find_one({"telegram_id": user_info.id})
    if not user:
        new_user = User(
            telegram_id=user_info.id,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            username=user_info.username
        )
        await db.users.insert_one(new_user.dict(by_alias=True))
    
    await update.message.reply_text(
        "Hi! I'm your personal mental health tracker. I'll check in with you every few hours. "
        "How are you feeling right now?",
        reply_markup=MOOD_KEYBOARD
    )

async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mood = update.message.text
    user_id = update.effective_user.id

    mood_entry = MoodEntry(user_id=user_id, mood=mood)
    await db.mood_entries.insert_one(mood_entry.dict(by_alias=True))

    await update.message.reply_text("Thank you for sharing. I'll check in again later.")

    # Optional: Get a dynamic follow-up question
    # next_question = await get_next_question(user_id)
    # await update.message.reply_text(next_question, reply_markup=MOOD_KEYBOARD)


async def check_in(bot, user_id: int) -> None:
    """Send a check-in message to a user."""
    question = await get_next_question(user_id)
    await bot.send_message(chat_id=user_id, text=question, reply_markup=MOOD_KEYBOARD)


def run_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mood))

    return application
