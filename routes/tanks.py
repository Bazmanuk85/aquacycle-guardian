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

    if not user_id:
        return RedirectResponse("/", status_code=303)

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


# VIEW TANK
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
        try:
            ammonia.append(float(t.ammonia))
            nitrite.append(float(t.nitrite))
            nitrate.append(float(t.nitrate))
            dates.append(t.created.strftime("%d %b"))
        except:
            pass

    warning = None

    if tests:

        latest = tests[-1]

        try:

            temp = float(latest.temperature)

            if temp > 30:
                warning = "Temperature warning: water too warm"

        except:
            pass

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "ammonia": ammonia,
            "nitrite": nitrite,
            "nitrate": nitrate,
            "dates": dates,
            "warning": warning
        }
    )


# ADD WATER TEST PAGE
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

    if ph < 0 or ph > 14:
        return RedirectResponse(f"/add-test/{tank_id}", status_code=303)

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
            "tank_id": tank_id
        }
    )


# SAVE WATER CHANGE
@router.post("/water-change/{tank_id}")
def add_water_change(
    tank_id: int,
    percent: int = Form(...)
):

    if percent < 1 or percent > 100:
        return RedirectResponse(f"/water-change/{tank_id}", status_code=303)

    db = SessionLocal()

    change = models.WaterChange(
        tank_id=tank_id,
        percent=percent,
        created=datetime.utcnow()
    )

    db.add(change)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)
