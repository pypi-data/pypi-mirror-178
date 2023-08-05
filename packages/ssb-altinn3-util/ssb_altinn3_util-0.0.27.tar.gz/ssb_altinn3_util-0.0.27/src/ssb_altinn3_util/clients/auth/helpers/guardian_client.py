import json

import ssb_altinn3_util.clients.auth.helpers.http_helper as http_client
from ssb_altinn3_util.clients.decorators.simple_exception_wrapper import (
    exception_handler,
)


class GuardianClient:
    def __init__(self):
        self.token_endpoint = f"http://maskinporten-guardian.dapla.svc.cluster.local/maskinporten/access-token"

    @exception_handler("Guardian Client")
    def get_token(self, keycloak_token: str) -> str:
        headers = {
            "Authorization": f"Bearer {keycloak_token}",
            "Content-Type": "application/json",
        }
        request_content = "{}"

        content = http_client.post(self.token_endpoint, headers, request_content)

        token: str = json.loads(content)["accessToken"]

        return token
