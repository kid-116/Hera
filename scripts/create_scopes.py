import os
import json
import sys

import requests

sys.path.append(os.path.join(
    os.path.dirname(__file__),
    "../"
))

from app.utils.oidc_client import WSO2Client


class Client(WSO2Client):
    def __init__(self, client_id, client_secret, is_host, admin, admin_pass):
        WSO2Client.__init__(self, client_id, client_secret, is_host)
        self.admin = admin
        self.admin_pass = admin_pass

    def create_scope(self, name, display_name, roles):
        request = requests.Request(
            'POST',
            f"{self.is_host}/api/identity/oauth2/v1.0/scopes",
            data=json.dumps({
                "name": name,
                "displayName": display_name,
                "bindings": roles
            }),
            headers={
                "content-Type": "application/json"
            },
            auth=(self.admin, self.admin_pass)
        )
        response = self._WSO2Client__session.send(request.prepare())
        return response

client = Client(
    os.getenv('WSO2_CLIENT_ID'),
    os.getenv('WSO2_CLIENT_SECRET'),
    os.getenv('WSO2_HOST'),
    os.getenv('WSO2_ADMIN'),
    os.getenv('WSO2_ADMIN_PASS'),
)

response = client.create_scope(
    "friends_view3",
    "friends_view",
    []
)
print(response)
