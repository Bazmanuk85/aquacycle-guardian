from fastapi import FastAPI

from database import engine
import models

from routes import auth
from routes import tanks

app = FastAPI()

# Create database tables automatically
models.Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router)
app.include_router(tanks.router)
