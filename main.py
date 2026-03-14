from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal
import models
from routes import tanks

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(tanks.router)


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None
        }
    )


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if not username or not password:

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Something fishy going on — please check username / password"
            }
        )

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user or user.password != password:

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Something fishy going on — please check username / password"
            }
        )

    response = RedirectResponse("/dashboard", status_code=303)

    response.set_cookie("user_id", str(user.id))
    response.set_cookie("username", user.username)

    return response


@app.get("/logout")
def logout():

    response = RedirectResponse("/", status_code=303)

    response.delete_cookie("user_id")
    response.delete_cookie("username")

    return response
