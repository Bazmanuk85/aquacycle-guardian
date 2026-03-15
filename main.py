from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

import models
from database import engine
from routes import auth
from routes import tanks

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(tanks.router)
