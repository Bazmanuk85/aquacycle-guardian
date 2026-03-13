from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# LOGIN PAGE
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# LOGIN ACTION
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user:
        user = models.User(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)

    response = RedirectResponse("/dashboard", status_code=303)

    response.set_cookie("user_id", str(user.id))
    response.set_cookie("username", username)

    return response


# LOGOUT
@app.get("/logout")
def logout():

    response = RedirectResponse("/", status_code=303)

    response.delete_cookie("user_id")
    response.delete_cookie("username")

    return response


# DASHBOARD
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    user_id = request.cookies.get("user_id")
    username = request.cookies.get("username")

    db = SessionLocal()

    tanks = db.query(models.Tank).filter(
        models.Tank.owner_id == user_id
    ).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tanks": tanks,
            "username": username
        }
    )


# CREATE TANK PAGE
@app.get("/create-tank", response_class=HTMLResponse)
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


# CREATE TANK
@app.post("/create-tank")
def create_tank(name: str = Form(...), volume: int = Form(...), request: Request = None):

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


# DELETE TANK
@app.get("/delete-tank/{tank_id}")
def delete_tank(tank_id: int):

    db = SessionLocal()

    tank = db.query(models.Tank).filter(
        models.Tank.id == tank_id
    ).first()

    if tank:
        db.delete(tank)
        db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# TANK PAGE
@app.get("/tank/{tank_id}", response_class=HTMLResponse)
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

    return templates.TemplateResponse(
