from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import auth
from routes import tanks

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(tanks.router)

# Static files (future use)
app.mount("/static", StaticFiles(directory="static"), name="static")
