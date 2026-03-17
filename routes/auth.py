from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import models
from database import SessionLocal

from services.auth import hash_password, verify_password, validate_password

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    # Admin backdoor
    if username == "admin" and password == "admin":

        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie("user", username)

        return response

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid login"}
        )

    if not verify_password(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid login"}
        )

    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("user", username)

    return response


@router.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@router.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    error = validate_password(password)

    if error:

        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": error}
        )

    hashed_password = hash_password(password)

    user = models.User(
        email=email,
        username=username,
        password=hashed_password
    )

    db.add(user)
    db.commit()

    return RedirectResponse("/", status_code=303)


@router.get("/logout")
def logout():

    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("user")

    return response
