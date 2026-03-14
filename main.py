from fastapi import FastAPI

from routes import auth
from routes import tanks

app = FastAPI()

# Register routers
app.include_router(auth.router)
app.include_router(tanks.router)
