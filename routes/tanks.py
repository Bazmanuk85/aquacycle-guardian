from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

import models
from database import SessionLocal

from services.analytics import (
    detect_cycle_stage,
    cycle_progress,
    ammonia_warning,
    temperature_alert,
    tank_health_score,
    adjusted_water_change_recommendation,
    maintenance_reminder
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# -----------------------------
# Database Session
# -----------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Dashboard
# -----------------------------

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):

    tanks = db.query(models.Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tanks": tanks
        }
    )


# -----------------------------
# Create Tank Page
# -----------------------------

@router.get("/create-tank")
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


# -----------------------------
# Create Tank Submit
# -----------------------------

@router.post("/create-tank")
def create_tank(
    request: Request,
    name: str = Form(...),
    tank_type: str = Form(...),
    db: Session = Depends(get_db)
):

    tank = models.Tank(
        name=name,
        tank_type=tank_type
    )

    db.add(tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# -----------------------------
# Tank Detail
# -----------------------------

@router.get("/tank/{tank_id}")
def tank_detail(request: Request, tank_id: int, db: Session = Depends(get_db)):

    tank = db.query(models.Tank).filter(models.Tank.id == tank_id).first()

    tests = (
        db.query(models.WaterTest)
        .filter(models.WaterTest.tank_id == tank_id)
        .order_by(models.WaterTest.timestamp)
        .all()
    )

    water_changes = (
        db.query(models.WaterChange)
        .filter(models.WaterChange.tank_id == tank_id)
        .order_by(models.WaterChange.timestamp)
        .all()
    )

    cycle_stage = detect_cycle_stage(tests)
    cycle_percent = cycle_progress(tests)

    ammonia_alert = ammonia_warning(tests)
    temp_alert = temperature_alert(tests)

    health_score = tank_health_score(tests)

    recommendation = adjusted_water_change_recommendation(
        tests,
        water_changes
    )

    maintenance = maintenance_reminder(
        water_changes,
        tests
    )

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests,
            "water_changes": water_changes,
            "cycle_stage": cycle_stage,
            "cycle_percent": cycle_percent,
            "ammonia_alert": ammonia_alert,
            "temp_alert": temp_alert,
            "health_score": health_score,
            "recommendation": recommendation,
            "maintenance": maintenance
        }
    )
