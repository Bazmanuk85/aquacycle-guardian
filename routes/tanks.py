from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/tank/{tank_id}", response_class=HTMLResponse)
def tank_page(request: Request, tank_id: int):

    db = SessionLocal()

    tank = db.query(models.Tank).filter(
        models.Tank.id == tank_id
    ).first()

    tests = db.query(models.WaterTest).filter(
        models.WaterTest.tank_id == tank_id
    ).order_by(models.WaterTest.created.asc()).all()

    changes = db.query(models.WaterChange).filter(
        models.WaterChange.tank_id == tank_id
    ).order_by(models.WaterChange.created.desc()).all()

    ammonia = []
    nitrite = []
    nitrate = []
    dates = []

    for t in tests:

        ammonia.append(float(t.ammonia))
        nitrite.append(float(t.nitrite))
        nitrate.append(float(t.nitrate))
        dates.append(t.created.strftime("%d %b"))


    # WATER CHANGE DATA

    last_change = None
    days_since_change = None
    dilution = 0

    if changes:

        latest = changes[0]

        last_change = latest.percent
        dilution = latest.percent / 100
        days_since_change = (datetime.utcnow() - latest.created).days


    cycle_stage = "No data"
    cycle_progress = 0
    tank_health = "Unknown"
    recommendation = "Add water test data"
    water_change_recommendation = None


    if tests:

        latest = tests[-1]

        ammonia_val = float(latest.ammonia)
        nitrite_val = float(latest.nitrite)
        nitrate_val = float(latest.nitrate)


        # APPLY WATER CHANGE DILUTION

        if dilution > 0:

            ammonia_val = ammonia_val * (1 - dilution)
            nitrite_val = nitrite_val * (1 - dilution)
            nitrate_val = nitrate_val * (1 - dilution)


        # CYCLE LOGIC

        if ammonia_val > 0.5 and nitrite_val == 0:

            cycle_stage = "Ammonia Spike"
            cycle_progress = 20

        elif nitrite_val > 0.5:

            cycle_stage = "Nitrite Spike"
            cycle_progress = 60

        elif nitrate_val > 5 and ammonia_val == 0 and nitrite_val == 0:

            cycle_stage = "Cycle Complete"
            cycle_progress = 100

        elif nitrate_val > 0:

            cycle_stage = "Nitrate Rising"
            cycle_progress = 80


        # HEALTH SCORE

        health = 100

        if ammonia_val > 0.25:
            health -= 40

        if nitrite_val > 0.25:
            health -= 30

        if nitrate_val > 40:
            health -= 20

        if health >= 80:
            tank_health = "Excellent"
        elif health >= 60:
            tank_health = "Good"
        elif health >= 40:
            tank_health = "Warning"
        else:
            tank_health = "Danger"


        # WATER CHANGE RECOMMENDATION

        if nitrate_val > 20:

            target = 10

            percent = int((1 - (target / nitrate_val)) * 100)

            if percent > 0:
                water_change_recommendation = percent

            recommendation = "Nitrate rising — water change recommended"


    # BUILD TIMELINE HISTORY

    history = []

    for t in tests:

        history.append({
            "timestamp": t.created,
            "date": t.created.strftime("%d %b %Y"),
            "event": f"Water Test — NH3:{t.ammonia} NO2:{t.nitrite} NO3:{t.nitrate}"
        })

    for c in changes:

        history.append({
            "timestamp": c.created,
            "date": c.created.strftime("%d %b %Y"),
            "event": f"Water Change {c.percent}%"
        })


    history.sort(key=lambda x: x["timestamp"], reverse=True)


    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "ammonia": ammonia,
            "nitrite": nitrite,
            "nitrate": nitrate,
            "dates": dates,
            "cycle_stage": cycle_stage,
            "cycle_progress": cycle_progress,
            "tank_health": tank_health,
            "recommendation": recommendation,
            "water_change_recommendation": water_change_recommendation,
            "last_change": last_change,
            "days_since_change": days_since_change,
            "history": history
        }
    )
