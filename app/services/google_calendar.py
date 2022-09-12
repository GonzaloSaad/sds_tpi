from app.services import oauth2

google_calendar_api = "https://www.googleapis.com/calendar/v3/users/me/calendarList"


def get_calendar(user_id: str):
    with oauth2.load(user_id) as session:
        response = session.get(google_calendar_api)
    return response.json()
