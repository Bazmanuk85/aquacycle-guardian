from fastapi import FastAPI

from database import engine
import models

from routes import auth
from routes import tanks


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth.router)
app.include_router(tanks.router)
