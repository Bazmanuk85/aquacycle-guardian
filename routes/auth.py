from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user or user.password != password:

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "something fishy going on please check username / password"
            }
        )

    response = RedirectResponse("/dashboard", status_code=303)

    response.set_cookie("user", username)

    return response
