from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from database import SessionLocal
from models import Tank, WaterTest, WaterChange

from services.analytics import (
    detect_cycle_stage,
    cycle_progress,
    nitrate_spike,
    ammonia_warning,
    temperature_alert,
    adjusted_water_change_recommendation,
    tank_health_score
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

    tanks = db.query(Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tanks": tanks}
    )


@router.get("/tank/{tank_id}")
def tank_detail(tank_id: int, request: Request, db: Session = Depends(get_db)):

    tank = db.query(Tank).filter(Tank.id == tank_id).first()

    tests = db.query(WaterTest).filter(
        WaterTest.tank_id == tank_id
    ).order_by(WaterTest.timestamp).all()

    water_changes = db.query(WaterChange).filter(
        WaterChange.tank_id == tank_id
    ).order_by(WaterChange.timestamp).all()

    cycle = detect_cycle_stage(tests)

    progress = cycle_progress(tests)

    ammonia_alert = ammonia_warning(tests)

    temp_alert = temperature_alert(tests)

    nitrate_values = [t.nitrate for t in tests if t.nitrate is not None]

    nitrate_alert = nitrate_spike(nitrate_values)

    recommendation = adjusted_water_change_recommendation(
        tests,
        water_changes
    )

    health = tank_health_score(tests)

    total_dilution = sum(c.percent for c in water_changes)

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests,
            "water_changes": water_changes,
            "cycle": cycle,
            "cycle_progress": progress,
            "nitrate_alert": nitrate_alert,
            "ammonia_alert": ammonia_alert,
            "temp_alert": temp_alert,
            "recommendation": recommendation,
            "health": health,
            "total_dilution": round(total_dilution,1)
        }
    )
