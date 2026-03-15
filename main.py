from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine
import models

from routes import auth
from routes import tanks

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(tanks.router)
