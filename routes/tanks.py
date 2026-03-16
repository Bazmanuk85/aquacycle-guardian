from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import models
from database import SessionLocal

from services.analytics import (
    adjusted_water_change_recommendation,
    tank_health_score,
    generate_ai_recommendations
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(request: Request):

    db = SessionLocal()

    tanks = db.query(models.Tank).all()

    tank_data = []

    for tank in tanks:

        tests = db.query(models.WaterTest)\
            .filter(models.WaterTest.tank_id == tank.id)\
            .order_by(models.WaterTest.timestamp)\
            .all()

        changes = db.query(models.WaterChange)\
            .filter(models.WaterChange.tank_id == tank.id)\
            .order_by(models.WaterChange.timestamp)\
            .all()

        recommendation = adjusted_water_change_recommendation(tests, changes)

        health = tank_health_score(tests)

        alerts = generate_ai_recommendations(tests)

        tank_data.append({
            "tank": tank,
            "health": health,
            "recommendation": recommendation,
            "tests": tests,
            "alerts": alerts
        })

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tank_data": tank_data
        }
    )


@router.get("/tank/{tank_id}")
def tank_detail(request: Request, tank_id: int):

    db = SessionLocal()

    tank = db.get(models.Tank, tank_id)

    tests = db.query(models.WaterTest)\
        .filter(models.WaterTest.tank_id == tank_id)\
        .order_by(models.WaterTest.timestamp)\
        .all()

    changes = db.query(models.WaterChange)\
        .filter(models.WaterChange.tank_id == tank_id)\
        .order_by(models.WaterChange.timestamp)\
        .all()

    fish = db.query(models.Fish)\
        .filter(models.Fish.tank_id == tank_id)\
        .all()

    recommendation = adjusted_water_change_recommendation(tests, changes)

    health = tank_health_score(tests)

    alerts = generate_ai_recommendations(tests)

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests,
            "changes": changes,
            "fish": fish,
            "recommendation": recommendation,
            "health": health,
            "alerts": alerts
        }
    )


@router.get("/tank/{tank_id}/add-fish")
def add_fish_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "add_fish.html",
        {"request": request, "tank_id": tank_id}
    )


@router.post("/tank/{tank_id}/add-fish")
def add_fish(
        tank_id: int,
        species: str = Form(...),
        quantity: int = Form(...)
):

    db = SessionLocal()

    fish = models.Fish(
        tank_id=tank_id,
        species=species,
        quantity=quantity
    )

    db.add(fish)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)
