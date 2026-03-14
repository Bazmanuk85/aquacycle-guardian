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


# DASHBOARD
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):

    tanks = db.query(models.Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tanks": tanks}
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
    name: str = Form(...),
    tank_type: str = Form(...),
    db: Session = Depends(get_db)
):

    tank = models.Tank(name=name, tank_type=tank_type)

    db.add(tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# VIEW TANK
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


# WATER TEST PAGE
@router.get("/add-test/{tank_id}", response_class=HTMLResponse)
def add_test_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "add_test.html",
        {"request": request, "tank_id": tank_id}
    )


# SAVE WATER TEST
@router.post("/add-test/{tank_id}")
def save_test(
    tank_id: int,
    ammonia: float = Form(...),
    nitrite: float = Form(...),
    nitrate: float = Form(...),
    ph: float = Form(...),
    temperature: float = Form(...),
    db: Session = Depends(get_db)
):

    new_test = models.WaterTest(
        tank_id=tank_id,
        ammonia=ammonia,
        nitrite=nitrite,
        nitrate=nitrate,
        ph=ph,
        temperature=temperature
    )

    db.add(new_test)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)


# WATER CHANGE PAGE
@router.get("/water-change/{tank_id}", response_class=HTMLResponse)
def water_change_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "water_change.html",
        {"request": request, "tank_id": tank_id}
    )


# SAVE WATER CHANGE
@router.post("/water-change/{tank_id}")
def save_water_change(
    tank_id: int,
    percent: float = Form(...),
    db: Session = Depends(get_db)
):

    change = models.WaterChange(
        tank_id=tank_id,
        percent=percent
    )

    db.add(change)
    db.commit()

    return RedirectResponse(f"/tank/{tank_id}", status_code=303)
