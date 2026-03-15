from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import models
from database import engine

from routes import auth
from routes import tanks

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(auth.router)
app.include_router(tanks.router)
