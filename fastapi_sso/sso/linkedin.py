"""LinkedIn SSO Oauth Helper class"""

from typing import TYPE_CHECKING, Dict, Optional

from fastapi_sso.sso.base import DiscoveryDocument, OpenID, SSOBase

if TYPE_CHECKING:
    import httpx


class LinkedInSSO(SSOBase):
    """Class providing login via LinkedIn SSO"""

    provider = "linkedin"
    scope = ["openid", "profile", "email"]
    additional_headers = {"accept": "application/json"}

    @property
    def _extra_query_params(self) -> Dict:
        return {"client_secret": self.client_secret}

    async def get_discovery_document(self) -> DiscoveryDocument:
        return {
            "authorization_endpoint": "https://www.linkedin.com/oauth/v2/authorization",
            "token_endpoint": "https://www.linkedin.com/oauth/v2/accessToken",
            "userinfo_endpoint": "https://api.linkedin.com/v2/userinfo",
        }

    async def openid_from_response(self, response: dict, session: Optional["httpx.AsyncClient"] = None) -> OpenID:
        return OpenID(
            email=response.get("email"),
            provider=self.provider,
            id=response["sub"],
            first_name=response["given_name"],
            last_name=response["family_name"],
            picture=response["picture"],
        )
