from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from database import engine
import models

from routes import auth
from routes import tanks

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Load route groups
app.include_router(auth.router)
app.include_router(tanks.router)
