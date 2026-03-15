from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):

    tanks = db.query(models.Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tanks": tanks}
    )


@router.get("/tank/{tank_id}")
def tank_detail(request: Request, tank_id: int, db: Session = Depends(get_db)):

    tank = db.query(models.Tank).filter(models.Tank.id == tank_id).first()

    tests = db.query(models.WaterTest)\
        .filter(models.WaterTest.tank_id == tank_id)\
        .order_by(models.WaterTest.timestamp)\
        .all()

    water_changes = db.query(models.WaterChange)\
        .filter(models.WaterChange.tank_id == tank_id)\
        .order_by(models.WaterChange.timestamp)\
        .all()

    cycle_stage = detect_cycle_stage(tests)
    cycle_percent = cycle_progress(tests)

    ammonia_alert = ammonia_warning(tests)
    temp_alert = temperature_alert(tests)

    health_score = tank_health_score(tests)

    recommendation = adjusted_water_change_recommendation(tests, water_changes)

    maintenance = maintenance_reminder(water_changes, tests)

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
