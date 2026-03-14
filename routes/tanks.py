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

    db = SessionLocal()

    tanks = db.query(models.Tank).filter(
        models.Tank.owner_id == user_id
    ).all()

    tank_data = []

    for tank in tanks:

        tests = db.query(models.WaterTest).filter(
            models.WaterTest.tank_id == tank.id
        ).all()

        health = 100

        if tests:

            last = tests[-1]

            try:
                if float(last.ammonia) > 0:
                    health -= 40

                if float(last.nitrite) > 0:
                    health -= 30

                if float(last.nitrate) > 40:
                    health -= 20
            except:
                pass

        tank_data.append({
            "tank": tank,
            "health": health
        })

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "tank_data": tank_data
        }
    )


@router.get("/create-tank", response_class=HTMLResponse)
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


@router.post("/create-tank")
def create_tank(request: Request, name: str = Form(...), volume: int = Form(...)):

    user_id = request.cookies.get("user_id")

    db = SessionLocal()

    tank = models.Tank(
        name=name,
        volume=volume,
        owner_id=user_id
    )

    db.add(tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


@router.get("/delete-tank/{tank_id}")
def delete_tank(tank_id: int):

    db = SessionLocal()

    tank = db.query(models.Tank).filter(
        models.Tank.id == tank_id
    ).first()

    if tank:
        db.delete(tank)
        db.commit()

    return RedirectResponse("/dashboard", status_code=303)
