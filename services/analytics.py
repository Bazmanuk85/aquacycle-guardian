from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import SessionLocal
import models

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


@router.get("/create-tank", response_class=HTMLResponse)
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


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
            "temperature": temperature
        }
    )


@router.get("/add-test/{tank_id}", response_class=HTMLResponse)
def add_test_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "add_test.html",
        {
            "request": request,
            "tank_id": tank_id
        }
    )


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
        temperature=str(temperature)
    )

    db.add(test)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)


@router.get("/water-change/{tank_id}", response_class=HTMLResponse)
def water_change_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "water_change.html",
        {
            "request": request,
            "tank_id": tank_id
        }
    )


@router.post("/water-change/{tank_id}")
def add_water_change(
    tank_id: int,
    percent: int = Form(...)
):

    db = SessionLocal()

    change = models.WaterChange(
        tank_id=tank_id,
        percent=percent
    )

    db.add(change)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)
