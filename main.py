from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Tank, WaterTest
from routes import auth, tanks

from fastapi.templating import Jinja2Templates

app = FastAPI()

# Keep routers unchanged
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


@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/login", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):

    username = request.cookies.get("user")

    if not username:
        return RedirectResponse(url="/login", status_code=302)

    tanks = db.query(Tank).filter(Tank.owner == username).all()

    healthy = 0
    warning = 0
    critical = 0

    tank_data = []

    for tank in tanks:

        latest_test = (
            db.query(WaterTest)
            .filter(WaterTest.tank_id == tank.id)
            .order_by(WaterTest.date.desc())
            .first()
        )

        status = "unknown"

        if latest_test:
            if latest_test.ammonia > 0 or latest_test.nitrite > 0:
                status = "critical"
                critical += 1
            elif latest_test.nitrate > 40:
                status = "warning"
                warning += 1
            else:
                status = "healthy"
                healthy += 1

        tank_data.append({
            "tank": tank,
            "latest_test": latest_test,
            "status": status
        })

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "tank_data": tank_data,
            "healthy_count": healthy,
            "warning_count": warning,
            "critical_count": critical
        }
    )
