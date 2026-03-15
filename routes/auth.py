from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if username == "admin" and password == "admin":

        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie("user", username)
        return response

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid login"}
    )


@router.get("/logout")
def logout():

    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("user")

    return response
