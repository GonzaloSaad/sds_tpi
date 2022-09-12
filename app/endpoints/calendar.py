from fastapi import APIRouter

from app.services import google_calendar

router = APIRouter(prefix="/google")


@router.get("/calendar/{user_id}")
def get_calendar(user_id: str):
    return google_calendar.get_calendar(user_id)
