from fastapi import FastAPI

from app.core.config import settings
from app.db.session import init_db

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
async def startup_event():
    # initialize DB / indexes if needed
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}
