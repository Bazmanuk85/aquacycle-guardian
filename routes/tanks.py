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


# -----------------------------
# Dashboard
# -----------------------------

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):

    tanks = db.query(Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tanks": tanks
        }
    )


# -----------------------------
# Create Tank
# -----------------------------

@router.get("/create-tank")
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


@router.post("/create-tank")
def create_tank(
    name: str = Form(...),
    tank_type: str = Form(...),
    db: Session = Depends(get_db)
):

    tank = Tank(
        name=name,
        tank_type=tank_type
    )

    db.add(tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# -----------------------------
# Delete Tank
# -----------------------------

@router.post("/delete-tank/{tank_id}")
def delete_tank(tank_id: int, db: Session = Depends(get_db)):

    tank = db.query(Tank).filter(Tank.id == tank_id).first()

    if tank:

        db.query(WaterTest).filter(
            WaterTest.tank_id == tank_id
        ).delete()

        db.query(WaterChange).filter(
            WaterChange.tank_id == tank_id
        ).delete()

        db.delete(tank)

        db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# -----------------------------
# Tank Detail
# -----------------------------

@router.get("/tank/{tank_id}")
def tank_detail(tank_id: int, request: Request, db: Session = Depends(get_db)):

    tank = db.query(Tank).filter(
        Tank.id == tank_id
    ).first()

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

    nitrate_values = [
        t.nitrate for t in tests if t.nitrate is not None
    ]

    nitrate_alert = nitrate_spike(nitrate_values)

    recommendation = adjusted_water_change_recommendation(
        tests,
        water_changes
    )

    health = tank_health_score(tests)

    total_dilution = sum(
        c.percent for c in water_changes
    )

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
            "total_dilution": round(total_dilution, 1)
        }
    )


# -----------------------------
# Water Tests
# -----------------------------

@router.get("/add-test/{tank_id}")
def add_test_page(tank_id: int, request: Request):

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
    ammonia: str = Form(""),
    nitrite: str = Form(""),
    nitrate: str = Form(""),
    ph: str = Form(""),
    temperature: str = Form(""),
    db: Session = Depends(get_db)
):

    if not any([ammonia, nitrite, nitrate, ph, temperature]):

        return RedirectResponse(
            f"/tank/{tank_id}",
            status_code=303
        )

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

    return RedirectResponse(
        f"/tank/{tank_id}",
        status_code=303
    )


# -----------------------------
# Water Change
# -----------------------------

@router.get("/water-change/{tank_id}")
def water_change_page(tank_id: int, request: Request):

    return templates.TemplateResponse(
        "water_change.html",
        {
            "request": request,
            "tank_id": tank_id
        }
    )


@router.post("/water-change/{tank_id}")
def water_change(
    tank_id: int,
    percent: float = Form(...),
    db: Session = Depends(get_db)
):

    wc = WaterChange(
        tank_id=tank_id,
        percent=percent
    )

    db.add(wc)

    db.commit()

    return RedirectResponse(
        f"/tank/{tank_id}",
        status_code=303
    )
