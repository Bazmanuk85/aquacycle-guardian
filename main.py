from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

import models
from database import engine, SessionLocal

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

app.mount("/static", StaticFiles(directory="static"), name="static")

# -----------------------------
# Include routers
# -----------------------------
app.include_router(auth.router)
app.include_router(tanks.router)

# -----------------------------
# Ensure default login exists
# -----------------------------
def create_default_user():

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == "admin"
    ).first()

    if not user:

        new_user = models.User(
            username="admin",
            password="admin"
        )

        db.add(new_user)
        db.commit()

    db.close()

create_default_user()
