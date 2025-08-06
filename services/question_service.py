from utils.db import db
from services.llm_service import get_llm_response
from datetime import datetime, timedelta

async def get_next_question(user_id: int) -> str:
    # Get the last mood entry
    last_mood_entry = await db.mood_entries.find_one(
        {"user_id": user_id},
        sort=[("timestamp", -1)]
    )

    if not last_mood_entry:
        return "How are you feeling right now?"

    last_mood = last_mood_entry['mood']
    prompt = f"The user's last mood was '{last_mood}'. Ask a gentle, open-ended follow-up question to explore why they might be feeling that way. Keep it short and inviting."
    question = get_llm_response(prompt)
    return question
