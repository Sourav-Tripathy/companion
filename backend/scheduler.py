from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.telegram_bot import check_in
from services.summary_service import get_daily_summary, get_weekly_summary
from utils.db import db

scheduler = AsyncIOScheduler()

async def send_check_in(bot, user_id):
    await check_in(bot, user_id)

async def schedule_check_ins(application):
    async for user in db.users.find():
        user_id = user['telegram_id']
        scheduler.add_job(send_check_in, 'interval', minutes=1, args=[application.bot, user_id], id=f"check_in_{user_id}")

async def send_summary(bot, user_id, summary_func):
    summary = await summary_func(user_id)
    await bot.send_message(chat_id=user_id, text=summary)

async def schedule_summaries(application):
    async for user in db.users.find():
        user_id = user['telegram_id']
        # Schedule daily summary
        scheduler.add_job(send_summary, CronTrigger(hour=21), args=[application.bot, user_id, get_daily_summary], id=f"daily_summary_{user_id}")
        # Schedule weekly summary
        scheduler.add_job(send_summary, CronTrigger(day_of_week='sun', hour=20), args=[application.bot, user_id, get_weekly_summary], id=f"weekly_summary_{user_id}")

def start_scheduler(application):
    scheduler.add_job(schedule_check_ins, 'date', args=[application])
    scheduler.add_job(schedule_summaries, 'date', args=[application])
    scheduler.start()
