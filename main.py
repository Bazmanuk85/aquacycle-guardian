from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Tank
from routes import auth, tanks

from fastapi.templating import Jinja2Templates

app = FastAPI()

app.include_router(auth.router)
app.include_router(tanks.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):

    username = request.cookies.get("user")

    if not username:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Please login"}
        )

    tanks = db.query(Tank).filter(Tank.owner == username).all()

    healthy = 0
    warning = 0
    critical = 0

    for tank in tanks:

        if hasattr(tank, "status"):

            if tank.status == "healthy":
                healthy += 1

            elif tank.status == "warning":
                warning += 1

            elif tank.status == "critical":
                critical += 1

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "tanks": tanks,
            "healthy_count": healthy,
            "warning_count": warning,
            "critical_count": critical
        }
    )
