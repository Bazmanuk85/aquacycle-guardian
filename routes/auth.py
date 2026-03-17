from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND

from database import get_db
from models import User
from services.auth import hash_password, verify_password, validate_password

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


# ------------------------
# Simulated Email Sender
# ------------------------
def send_verification_email(email: str, username: str):
    print(f"[EMAIL SIMULATION] Sending verification email to {email} for user {username}")


# ------------------------
# REGISTER PAGE
# ------------------------
@router.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "errors": []}
    )


# ------------------------
# REGISTER POST
# ------------------------
@router.post("/register", response_class=HTMLResponse)
def register_post(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    errors = []

    # Username validation
    if len(username) < 3:
        errors.append("Username must be at least 3 characters long")

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        errors.append("Username already exists")

    # Email validation
    if "@" not in email:
        errors.append("Please enter a valid email address")

    # ✅ FIXED PASSWORD VALIDATION
    password_error = validate_password(password)
    if password_error:
        errors.append(password_error)

    # Return errors if any
    if errors:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "errors": errors,
                "username": username,
                "email": email
            }
        )

    # Create user
    hashed_pw = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()

    # Simulated email
    send_verification_email(email, username)

    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)


# ------------------------
# LOGIN PAGE
# ------------------------
@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# ------------------------
# LOGIN POST
# ------------------------
@router.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Admin backdoor
    if username == "admin" and password == "admin":
        response = RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)
        response.set_cookie(key="user", value="admin")
        return response

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password"
            }
        )

    response = RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)
    response.set_cookie(key="user", value=user.username)

    return response


# ------------------------
# LOGOUT
# ------------------------
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=HTTP_302_FOUND)
    response.delete_cookie("user")
    return response
