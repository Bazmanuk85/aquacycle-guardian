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
    recommend_water_change,
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


@router.get("/create-tank")
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


@router.post("/create-tank")
def create_tank(name: str = Form(...), tank_type: str = Form(...), db: Session = Depends(get_db)):

    tank = Tank(name=name, tank_type=tank_type)

    db.add(tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


@router.get("/tank/{tank_id}")
def tank_detail(tank_id: int, request: Request, db: Session = Depends(get_db)):

    tank = db.query(Tank).filter(Tank.id == tank_id).first()

    if not tank:
        return RedirectResponse("/dashboard", status_code=303)

    tests = db.query(WaterTest).filter(WaterTest.tank_id == tank_id).all()

    water_changes = db.query(WaterChange).filter(WaterChange.tank_id == tank_id).all()

    cycle = detect_cycle_stage(tests)

    progress = cycle_progress(tests)

    nitrate_alert = nitrate_spike(tests)

    ammonia_alert = ammonia_warning(tests)

    temp_alert = temperature_alert(tests)

    recommendation = recommend_water_change(tests)

    health = tank_health_score(tests)

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
            "health": health
        }
    )


@router.get("/add-test/{tank_id}")
def add_test_page(tank_id: int, request: Request):

    return templates.TemplateResponse(
        "add_test.html",
        {"request": request, "tank_id": tank_id}
    )


@router.post("/add-test/{tank_id}")
def add_test(
    tank_id: int,
    ammonia: str = Form(None),
    nitrite: str = Form(None),
    nitrate: str = Form(None),
    ph: str = Form(None),
    temperature: str = Form(None),
    db: Session = Depends(get_db)
):

    test = WaterTest(
        tank_id=tank_id,
        ammonia=float(ammonia) if ammonia else None,
        nitrite=float(nitrite) if nitrite else None,
        nitrate=float(nitrate) if nitrate else None,
        ph=float(ph) if ph else None,
        temperature=float(temperature) if temperature else None
    )

    db.add(test)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)


@router.get("/water-change/{tank_id}")
def water_change_page(tank_id: int, request: Request):

    return templates.TemplateResponse(
        "water_change.html",
        {"request": request, "tank_id": tank_id}
    )


@router.post("/water-change/{tank_id}")
def water_change(tank_id: int, percent: float = Form(...), db: Session = Depends(get_db)):

    wc = WaterChange(tank_id=tank_id, percent=percent)

    db.add(wc)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)
