from fastapi import FastAPI

from ..routers import health, user

app = FastAPI()

app.include_router(health.router)
app.include_router(user.router)
