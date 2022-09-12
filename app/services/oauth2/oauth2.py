import functools
from contextlib import contextmanager
from logging import getLogger
from typing import Any, Dict, List

from requests import Session
from requests_oauthlib import OAuth2Session

from app.services import crypto

from . import database
from .schemas import OAuth2State, OAuth2Token
from .settings import (calendar_scope, google_oauth2_client,
                       google_oauth2_server)

logger = getLogger()


def get_authorization_url(user_id: str) -> str:
    """
    Gets the authorization url for the authorization code flow in OAuth2.

    Docs:
        - https://auth0.com/docs/flows/authorization-code-flow

    Args:
        user_id: id of the user to create the authorization URL

    Returns:
        str: the authorization URL
    """

    state = _create_state(user_id)
    with _create_session(scope=calendar_scope) as session:
        authorization_url, _ = session.authorization_url(
            google_oauth2_server.authorization_url,
            state=state,
            **google_oauth2_client.authorization_args
        )

    return authorization_url


def process_callback(scope: str, state: str, code: str):
    """
    Fetches a token from the OAuth2 server based on the authorization response callback and saves the
    token into the OAuth2Token table.

    Args:
        scope (list): list of scopes to claim the token
        state (str): token sent to the OAuth2 server
        code (str): code received from the OAuth2 server

    Returns:
        str: url to redirect the call to
    """

    session_state = _parse_state(state)

    authorization_response = _create_authorization_response(code, scope, state)
    token = _fetch_token(authorization_response)

    database.insert(session_state.user_id, token)
    return "http://localhost:8080"


@contextmanager
def load(user_id: str) -> Session:
    """
    Loads an OAuth2 session from an existing OAuth2Token.

    Args:
        user_id (str): id of the customer to get the session.

    Returns:
        Session
    """
    token = database.get_by_user(user_id)
    token_updater = functools.partial(_token_updater, user_id)
    session = _create_session(token_updater=token_updater, token=token.dict())
    yield session


def _create_authorization_response(code: str, scope: str, state: str):
    return (
        f"http://localhost:8080/oauth2/callback?"
        f"state={state}&"
        f"code={code}&"
        f"scope={scope}"
    )


def _fetch_token(authorization_response: str) -> OAuth2Token:
    with _create_session() as session:
        raw_token = session.fetch_token(
            google_oauth2_server.token_url,
            authorization_response=authorization_response,
            client_secret=google_oauth2_client.client_secret,
        )
        logger.warning(raw_token)

    token = OAuth2Token.parse_obj(raw_token)
    return token


def _create_state(user_id: str) -> str:
    state = OAuth2State(user_id=user_id)
    return crypto.encrypt(data=state.json())


def _parse_state(state: str) -> OAuth2State:
    decrypted_state = crypto.decrypt(token=state)
    parsed_state = OAuth2State.parse_raw(decrypted_state)
    return parsed_state


def _create_session(*, state: str = None, scope: List[str] = None, token_updater=None, token=None) -> OAuth2Session:
    """
    Creates an OAuth2Session based on specific configuration of server/client.

    Args:
        state (str): string representing the state sent to the server. Mainly used during authorization

    Returns:
        OAuth2Session
    """
    return OAuth2Session(
        client_id=google_oauth2_client.client_id,
        redirect_uri="http://localhost:8080/oauth2/callback",
        auto_refresh_url=google_oauth2_server.token_url,
        auto_refresh_kwargs=google_oauth2_client.auto_refresh_kwargs,
        token=token,
        state=state,
        scope=scope,
        token_updater=token_updater,
    )


def _token_updater(user_id: str, token: Dict[str, Any]):
    parsed_token = OAuth2Token.parse_obj(token)
    database.update_by_user_id(user_id=user_id, token=parsed_token)
