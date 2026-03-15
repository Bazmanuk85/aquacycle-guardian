from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

import models
from database import engine

from routes import auth
from routes import tanks

app = FastAPI()

# -----------------------------
# Create database tables
# -----------------------------
models.Base.metadata.create_all(bind=engine)

# -----------------------------
# Ensure static folder exists
# -----------------------------
if not os.path.exists("static"):
    os.makedirs("static")

# -----------------------------
# Mount static files
# -----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# -----------------------------
# Register routers
# -----------------------------
app.include_router(auth.router)
app.include_router(tanks.router)
