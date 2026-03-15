from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

import models
from database import engine, SessionLocal
from routes import auth
from routes import tanks

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(auth.router)
app.include_router(tanks.router)


# -------------------------
# Ensure default login user
# -------------------------
def ensure_admin():

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == "admin"
    ).first()

    if not user:
        admin = models.User(
            username="admin",
            password="admin"
        )
        db.add(admin)
        db.commit()

    db.close()


ensure_admin()
