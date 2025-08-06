from fastapi import FastAPI
from bot.telegram_bot import run_bot
from backend.routes import router
from backend.scheduler import start_scheduler
import uvicorn
from contextlib import asynccontextmanager

telegram_app = run_bot()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    await telegram_app.initialize()
    await telegram_app.updater.start_polling()
    await telegram_app.start()
    start_scheduler(telegram_app)
    yield
    # On shutdown
    await telegram_app.stop()
    await telegram_app.updater.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
