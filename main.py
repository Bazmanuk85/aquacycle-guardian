from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import Base, engine

from routes import auth
from routes import tanks


app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(tanks.router)


# Static files (if you have css/js)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Root redirect
@app.get("/")
def root():
    return RedirectResponse(url="/login")
