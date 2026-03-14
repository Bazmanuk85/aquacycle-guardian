from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import SessionLocal
import models

from fastapi.templating import Jinja2Templates

from services.analytics import detect_cycle_stage, analyze_water_quality

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tank/{tank_id}", response_class=HTMLResponse)
def tank_detail(request: Request, tank_id: int, db: Session = Depends(get_db)):

    tank = db.query(models.Tank).filter(models.Tank.id == tank_id).first()

    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")

    tests = db.query(models.WaterTest).filter(
        models.WaterTest.tank_id == tank_id
    ).all()

    water_changes = db.query(models.WaterChange).filter(
        models.WaterChange.tank_id == tank_id
    ).all()

    cycle_stage, cycle_percent = detect_cycle_stage(tests)

    alerts, recommendations, health_score = analyze_water_quality(tests)

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests,
            "water_changes": water_changes,
            "cycle_stage": cycle_stage,
            "cycle_percent": cycle_percent,
            "alerts": alerts,
            "recommendations": recommendations,
            "health_score": health_score
        }
    )
