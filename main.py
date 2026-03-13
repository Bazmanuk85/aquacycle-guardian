from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if user:
        return RedirectResponse("/dashboard", status_code=303)

    new_user = models.User(username=username, password=password)
    db.add(new_user)
    db.commit()

    return RedirectResponse("/dashboard", status_code=303)


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
