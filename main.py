from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# ---------------- LOGIN ----------------

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


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

    return response


# ---------------- DASHBOARD ----------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    user_id = request.cookies.get("user_id")

    db = SessionLocal()

    tanks = db.query(models.Tank).filter(
        models.Tank.owner_id == user_id
    ).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tanks": tanks
        }
    )


# ---------------- CREATE TANK ----------------

@app.get("/create-tank", response_class=HTMLResponse)
def create_tank_page(request: Request):
    return templates.TemplateResponse("create_tank.html", {"request": request})


@app.post("/create-tank")
def create_tank(request: Request, name: str = Form(...), volume: int = Form(...)):

    user_id = request.cookies.get("user_id")

    db = SessionLocal()

    new_tank = models.Tank(
        name=name,
        volume=volume,
        owner_id=user_id
    )

    db.add(new_tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# ---------------- DELETE TANK ----------------

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


# ---------------- TANK PAGE ----------------

@app.get("/tank/{tank_id}", response_class=HTMLResponse)
def tank_page(request: Request, tank_id: int):

    db = SessionLocal()

    tank = db.query(models.Tank).filter(
        models.Tank.id == tank_id
    ).first()

    tests = db.query(models.WaterTest).filter(
        models.WaterTest.tank_id == tank_id
    ).all()

    return templates.TemplateResponse(
        "tank.html",
        {
            "request": request,
            "tank": tank,
            "tests": tests
        }
    )


# ---------------- ADD WATER TEST ----------------

@app.get("/add-test/{tank_id}", response_class=HTMLResponse)
def add_test_page(request: Request, tank_id: int):

    return templates.TemplateResponse(
        "add_test.html",
        {
            "request": request,
            "tank_id": tank_id
        }
    )


@app.post("/add-test/{tank_id}")
def add_test(
    tank_id: int,
    ammonia: str = Form(...),
    nitrite: str = Form(...),
    nitrate: str = Form(...),
    ph: str = Form(...),
    temperature: str = Form(...)
):

    db = SessionLocal()

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
