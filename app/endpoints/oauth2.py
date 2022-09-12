from http import HTTPStatus

from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from pydantic.types import UUID4

from app.services import oauth2

router = APIRouter(prefix="/oauth2")


@router.get("/auth", response_class=RedirectResponse, status_code=HTTPStatus.FOUND)
def oauth2_auth(
        user_id: UUID4 = Query(
            title="User ID",
            description="ID of the user to authorize",
        ),
):
    return oauth2.get_authorization_url(str(user_id))


@router.get("/callback", response_class=RedirectResponse, status_code=HTTPStatus.FOUND)
def oauth2_callback(
        state: str = Query(
            title="OAuth2 State",
            description="State sent to the oauth2 server",
        ),
        code: str = Query(
            title="OAuth2 Code",
            description="Code from the oauth2 server",
        ),
        scope: str = Query(
            title="OAuth2 Scope",
            description="Scope authorized by the oauth2 server",
        ),

):
    redirect_url = oauth2.process_callback(scope, state, code)
    return redirect_url
