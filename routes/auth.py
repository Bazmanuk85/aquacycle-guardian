from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import SessionLocal
import models

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None}
    )


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    db = SessionLocal()

    if not username or not password:

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Something fishy going on please check username / password"
            }
        )

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user and username == "admin" and password == "admin":

        user = models.User(
            username="admin",
            password="admin"
        )

        db.add(user)
        db.commit()

    if not user or user.password != password:

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Something fishy going on please check username / password"
            }
        )

    response = RedirectResponse("/dashboard", status_code=303)

    response.set_cookie("user_id", str(user.id))
    response.set_cookie("username", user.username)

    return response


@router.get("/logout")
def logout():

    response = RedirectResponse("/", status_code=303)

    response.delete_cookie("user_id")
    response.delete_cookie("username")

    return response
