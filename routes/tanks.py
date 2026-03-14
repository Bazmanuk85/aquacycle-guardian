from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models
from datetime import datetime

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# DASHBOARD
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
            "tanks": tanks
        }
    )


# CREATE TANK PAGE
@router.get("/create-tank", response_class=HTMLResponse)
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


# CREATE TANK
@router.post("/create-tank")
def create_tank(
    request: Request,
    name: str = Form(...),
    volume: int = Form(...),
    tank_type: str = Form(...)
):

    user_id = request.cookies.get("user_id")

    db = SessionLocal()

    tank = models.Tank(
        name=name,
        volume=volume,
        tank_type=tank_type,
        owner_id=int(user_id)
    )

    db.add(tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# TANK PAGE
@router.get("/tank/{tank_id}", response_class=HTMLResponse)
def tank_page(request: Request, tank_id: int):

    db = SessionLocal()

    tank = db.query(models.Tank).filter(
        models.Tank.id == tank_id
    ).first()

    tests = db.query(models.WaterTest).filter(
        models.WaterTest.tank_id == tank_id
    ).all()

    ammonia = []
    nitrite = []
    nitrate = []
    dates = []

    for t in tests:

        ammonia.append(float(t.ammonia))
        nitrite.append(float(t.nitrite))
        nitrate.append(float(t.nitrate))
        dates.append(t.created.strftime("%d %b"))

    cycle_stage = "No data"
    cycle_progress = 0
    tank_health = "Unknown"
    recommendation = "Add water test data"

    if tests:

        latest = tests[-1]

        a = float(latest.ammonia)
        ni = float(latest.nitrite)
        na = float(latest.nitrate)

        if a > 0.5 and ni == 0:
            cycle_stage = "Ammonia Spike"
            cycle_progress = 20

        elif ni > 0.5:
            cycle_stage = "Nitrite Spike"
            cycle_progress = 60

        elif na > 5 and a == 0 and ni == 0:
            cycle_stage = "Cycle Complete"
            cycle_progress = 100

        elif na > 0:
            cycle_stage = "Nitrate Rising"
            cycle_progress = 80

        health_score = 100

        if a > 0.25:
            health_score -= 40

        if ni > 0.25:
            health_score -= 30

        if na > 40:
            health_score -= 20

        if health_score >= 80:
            tank_health = "Excellent"

        elif health_score >= 60:
            tank_health = "Good"

        elif health_score >= 40:
            tank_health = "Warning"

        else:
            tank_health = "Danger"

        if a > 0.5 or ni > 0.5:
            recommendation = "Tank cycling — avoid water changes unless emergency"

        elif na > 40:
            recommendation = "Perform a 25% water change"

        elif na > 20:
            recommendation = "Monitor nitrate — water change soon"

        else:
            recommendation = "Tank stable"

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
            "recommendation": recommendation
        }
    )


# ADD TEST PAGE
@router.get("/add-test/{tank_id}", response_class=HTMLResponse)
def add_test_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "add_test.html",
        {
            "request": request,
            "tank_id": tank_id
        }
    )


# SAVE WATER TEST
@router.post("/add-test/{tank_id}")
def add_test(
    tank_id: int,
    ammonia: float = Form(...),
    nitrite: float = Form(...),
    nitrate: float = Form(...),
    ph: float = Form(...),
    temperature: float = Form(...)
):

    db = SessionLocal()

    test = models.WaterTest(
        tank_id=tank_id,
        ammonia=str(ammonia),
        nitrite=str(nitrite),
        nitrate=str(nitrate),
        ph=str(ph),
        temperature=str(temperature),
        created=datetime.utcnow()
    )

    db.add(test)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)


# WATER CHANGE PAGE
@router.get("/water-change/{tank_id}", response_class=HTMLResponse)
def water_change_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "water_change.html",
        {
            "request": request,
            "tank_id": tank_id,
            "error": None
        }
    )


# SAVE WATER CHANGE
@router.post("/water-change/{tank_id}")
def add_water_change(
    request: Request,
    tank_id: int,
    percent: int = Form(...)
):

    if percent > 100:

        return templates.TemplateResponse(
            "water_change.html",
            {
                "request": request,
                "tank_id": tank_id,
                "error": "Cannot exceed 100%!!"
            }
        )

    db = SessionLocal()

    change = models.WaterChange(
        tank_id=tank_id,
        percent=percent,
        created=datetime.utcnow()
    )

    db.add(change)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)
