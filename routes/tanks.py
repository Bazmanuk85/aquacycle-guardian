from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import SessionLocal
import models
from fastapi.templating import Jinja2Templates

from services.analytics import detect_cycle_stage

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
        {
            "request": request,
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
    name: str = Form(...),
    tank_type: str = Form(...),
    db: Session = Depends(get_db)
):
    tank = models.Tank(
        name=name,
        tank_type=tank_type
    )

    db.add(tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# TANK DETAILS
@router.get("/tank/{tank_id}", response_class=HTMLResponse)
def tank_detail(request: Request, tank_id: int, db: Session = Depends(get_db)):

    tank = db.query(models.Tank).filter(models.Tank.id == tank_id).first()

    if tank is None:
        raise HTTPException(status_code=404, detail="Tank not found")

    tests = db.query(models.WaterTest).filter(
        models.WaterTest.tank_id == tank_id
    ).all()

    water_changes = db.query(models.WaterChange).filter(
        models.WaterChange.tank_id == tank_id
    ).all()

    cycle_stage, cycle_percent = detect_cycle_stage(tests)

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests,
            "water_changes": water_changes,
            "cycle_stage": cycle_stage,
            "cycle_percent": cycle_percent
        }
    )
