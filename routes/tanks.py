from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal

from services.analytics import (
    adjusted_water_change_recommendation,
    tank_health_score
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def dashboard(request: Request):

    database = SessionLocal()
    tanks = database.query(models.Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tanks": tanks}
    )


@router.get("/create-tank")
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


@router.post("/create-tank")
def create_tank(name: str = Form(...), tank_type: str = Form(...)):

    database = SessionLocal()

    tank = models.Tank(name=name, tank_type=tank_type)

    database.add(tank)
    database.commit()

    return RedirectResponse("/dashboard", status_code=303)


@router.get("/tank/{tank_id}")
def tank_detail(request: Request, tank_id: int):

    database = SessionLocal()

    tank = database.query(models.Tank).get(tank_id)

    tests = database.query(models.WaterTest)\
        .filter(models.WaterTest.tank_id == tank_id)\
        .order_by(models.WaterTest.timestamp)\
        .all()

    changes = database.query(models.WaterChange)\
        .filter(models.WaterChange.tank_id == tank_id)\
        .order_by(models.WaterChange.timestamp)\
        .all()

    recommendation = adjusted_water_change_recommendation(tests, changes)

    health = tank_health_score(tests)

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests,
            "changes": changes,
            "recommendation": recommendation,
            "health": health
        }
    )
