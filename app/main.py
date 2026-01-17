


from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import init_db
# include routers
from app.api.v1.routes import auth as auth_router
from app.api.v1.routes import users as users_router
# openapi utils
from app.utils_openapi import generate_openapi_json



@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize DB / indexes if needed
    init_db()
    # 生成 openapi.json
    generate_openapi_json(app, output_path="openapi.json")
    yield



app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)



# register API routers
app.include_router(auth_router.router)
app.include_router(users_router.router)



@app.get("/health")
def health():
    return {"status": "ok"}
