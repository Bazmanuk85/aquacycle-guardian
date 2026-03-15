from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal

router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):

    tanks = db.query(models.Tank).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "tanks": tanks
        }
    )
