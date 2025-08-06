from utils.db import db
from services.llm_service import get_llm_response
from datetime import datetime, timedelta

async def get_summary(user_id: int, time_delta: timedelta) -> str:
    now = datetime.now()
    start_time = now - time_delta
    mood_entries = await db.mood_entries.find({
        "user_id": user_id,
        "timestamp": {"$gte": start_time}
    }).to_list(length=100)

    if not mood_entries:
        return "No mood entries found for this period."

    moods = [entry['mood'] for entry in mood_entries]
    prompt = f"Here are the recent moods of a user: {', '.join(moods)}. Please provide a gentle and supportive summary of their mood trend."
    summary = get_llm_response(prompt)
    return summary

async def get_daily_summary(user_id: int) -> str:
    return await get_summary(user_id, timedelta(days=1))

async def get_weekly_summary(user_id: int) -> str:
    return await get_summary(user_id, timedelta(weeks=1))
