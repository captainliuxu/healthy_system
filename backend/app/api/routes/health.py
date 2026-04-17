from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.response import success_response

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    return success_response(
        data={"service": "ok"},
        message="service is running",
    )


@router.get("/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return success_response(
        data={"database": "connected"},
        message="database is ok",
    )