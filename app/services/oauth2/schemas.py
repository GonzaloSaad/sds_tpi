from typing import List, Optional

from pydantic import BaseModel, validator


class OAuth2State(BaseModel):
    user_id: str

class OAuth2Token(BaseModel):
    """
    Model that represents an OAuth2 Token

    ---
    The OAuth2 framework includes the following fields:
    - access_token (Required)
    - token_type (Required)
    - expires_in (Recommended)
    - refresh_token (Optional)
    - scope (Optional)

    Since OAuth2 is a delegation framework, that means that
    the granted application can act in behalf of the user without
    knowing the user.

    Docs:
    https://www.oauth.com/oauth2-servers/access-tokens/
    https://www.oauth.com/oauth2-servers/access-tokens/access-token-response/

    ---
    OpenID Connect
    This Authentication protocol adds an identity layer on top of OAuth2.
    Because of that it adds the following field:
    - id_token (JWT)

    Docs:
    https://www.oauth.com/oauth2-servers/openid-connect/
    https://www.oauth.com/oauth2-servers/openid-connect/id-tokens/

    ---
    Other fields:
    - expires_at (Required)
    It is a field calculated by the requests_oauthlib used in this service

    More Reading:
    https://auth0.com/docs/tokens
    """

    access_token: str
    expires_in: int
    expires_at: float
    refresh_token: str
    scope: List[str]
    token_type: str
    id_token: Optional[str]

    @validator("scope", pre=True)
    def _scope_as_list(cls, value):  # pylint: disable=no-self-argument,no-self-use
        if isinstance(value, set):
            return list(value)
        return value
