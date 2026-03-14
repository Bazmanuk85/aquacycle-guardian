from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models
from datetime import datetime

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

    alerts = []

    for tank in tanks:

        latest_test = db.query(models.WaterTest).filter(
            models.WaterTest.tank_id == tank.id
        ).order_by(models.WaterTest.created.desc()).first()

        latest_change = db.query(models.WaterChange).filter(
            models.WaterChange.tank_id == tank.id
        ).order_by(models.WaterChange.created.desc()).first()


        # WATER CHANGE ALERTS

        if latest_change:

            days = (datetime.utcnow() - latest_change.created).days

            alerts.append(
                f"{tank.name}: last water change {days} days ago"
            )

            if days >= 7:

                alerts.append(
                    f"{tank.name}: water change recommended"
                )


        # WATER TEST ALERTS

        if latest_test:

            nitrate = float(latest_test.nitrate)
            ammonia = float(latest_test.ammonia)
            nitrite = float(latest_test.nitrite)

            alerts.append(
                f"{tank.name}: Nitrate level {nitrate} ppm"
            )

            if nitrate >= 40:

                alerts.append(
                    f"{tank.name}: HIGH nitrate — perform water change"
                )

            if ammonia > 0.25:

                alerts.append(
                    f"{tank.name}: Ammonia detected ⚠"
                )

            if nitrite > 0.25:

                alerts.append(
                    f"{tank.name}: Nitrite spike ⚠"
                )


    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "tanks": tanks,
            "alerts": alerts
        }
    )
