from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import SessionLocal
import models

from services.analytics import detect_cycle_stage

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    user_id = request.cookies.get("user_id")
    username = request.cookies.get("username")

    if not user_id:
        return RedirectResponse("/", status_code=303)

    db = SessionLocal()

    tanks = db.query(models.Tank).filter(
        models.Tank.owner_id == int(user_id)
    ).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "tanks": tanks,
            "alerts": []
        }
    )


@router.get("/tank/{tank_id}", response_class=HTMLResponse)
def tank_page(request: Request, tank_id: int):

    db = SessionLocal()

    tank = db.query(models.Tank).filter(
        models.Tank.id == tank_id
    ).first()

    tests = db.query(models.WaterTest).filter(
        models.WaterTest.tank_id == tank_id
    ).order_by(models.WaterTest.created).all()

    changes = db.query(models.WaterChange).filter(
        models.WaterChange.tank_id == tank_id
    ).all()

    # Graph Data
    labels = []
    ammonia = []
    nitrite = []
    nitrate = []
    ph = []
    temperature = []

    for t in tests:

        labels.append(t.created.strftime("%d %b"))

        ammonia.append(float(t.ammonia))
        nitrite.append(float(t.nitrite))
        nitrate.append(float(t.nitrate))
        ph.append(float(t.ph))
        temperature.append(float(t.temperature))

    # Cycle intelligence
    cycle_stage, cycle_progress = detect_cycle_stage(tests)

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests,
            "changes": changes,
            "labels": labels,
            "ammonia": ammonia,
            "nitrite": nitrite,
            "nitrate": nitrate,
            "ph": ph,
            "temperature": temperature,
            "cycle_stage": cycle_stage,
            "cycle_progress": cycle_progress
        }
    )
