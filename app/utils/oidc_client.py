import requests


class WSO2Client:
    def __init__(self, client_id, client_secret, is_host):
        self.is_host = is_host

        self.client_id = client_id

        self.token_url = f"{self.is_host}/oauth2/token"

        self.__session = requests.Session()
        self.__session.verify = False

        self.__client_auth = (
            self.client_id,
            client_secret
        )

        self.__client_token = self.__get_client_token()

    def __get_client_token(self):
        request = requests.Request(
            'POST',
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "scope": "internal_user_mgt_list"
            },
            auth=self.__client_auth,
        )
        response = self.__session.send(request.prepare())
        response = response.json()
        print(response)
        return response["access_token"]

    def username_exists(self, username):
        request = requests.Request(
            'GET',
            f"{self.is_host}/t/carbon.super/scim2/Users",
            headers={
                "Authorization": f"Bearer {self.__client_token}"
            },
            params={
                "attributes": "userName",
                "filter": f"userName eq {username}"
            }
        )
        response = self.__session.send(request.prepare())
        response = response.json()
        assert response['totalResults'] <= 1
        if response['totalResults'] == 0:
            return False
        resource, = response['Resources']
        return resource['userName'] == username
