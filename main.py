from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database import engine, SessionLocal
import models

# create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# template folder
templates = Jinja2Templates(directory="templates")


# LOGIN PAGE
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# LOGIN ACTION
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user:
        new_user = models.User(username=username, password=password)
        db.add(new_user)
        db.commit()

    return RedirectResponse("/dashboard", status_code=303)


# DASHBOARD
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    db = SessionLocal()

    tanks = db.query(models.Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tanks": tanks
        }
    )


# CREATE TANK PAGE
@app.get("/create-tank", response_class=HTMLResponse)
def create_tank_page(request: Request):

    return templates.TemplateResponse(
        "create_tank.html",
        {"request": request}
    )


# CREATE TANK ACTION
@app.post("/create-tank")
def create_tank(name: str = Form(...), volume: int = Form(...)):

    db = SessionLocal()

    new_tank = models.Tank(
        name=name,
        volume=volume,
        owner_id=1
    )

    db.add(new_tank)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)
