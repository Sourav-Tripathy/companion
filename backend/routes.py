from fastapi import APIRouter
from services.summary_service import get_daily_summary, get_weekly_summary
from services.question_service import get_next_question

router = APIRouter()

@router.get("/summary/daily/{user_id}")
async def daily_summary(user_id: int):
    summary = await get_daily_summary(user_id)
    return {"user_id": user_id, "summary": summary}

@router.get("/summary/weekly/{user_id}")
async def weekly_summary(user_id: int):
    summary = await get_weekly_summary(user_id)
    return {"user_id": user_id, "summary": summary}

@router.get("/question/next/{user_id}")
async def next_question(user_id: int):
    question = await get_next_question(user_id)
    return {"user_id": user_id, "question": question}
