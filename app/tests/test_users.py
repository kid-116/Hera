import os
import sys
import random

import pandas as pd
import pytest

sys.path.append(os.path.join(
    os.path.dirname(__file__),
    ".."
))

from utils.oidc_client import WSO2Client


@pytest.fixture
def is_client():
    return WSO2Client(
        os.environ['WSO2_CLIENT_ID'],
        os.environ['WSO2_CLIENT_SECRET'],
        os.environ['WSO2_HOST']
    )


users = pd.read_csv(os.path.join(
    os.path.dirname(__file__), "resources/users.csv"))
users = list(users.itertuples(index=False))

@pytest.mark.parametrize("name,email,phone,password", users)
def test_user_register(is_client, name, email, phone, password):
    response = is_client.register_user(
        name,
        email,
        phone,
        password
    )
    assert response.status_code == 201


name, _, _, password = random.choice(users)

@pytest.mark.parametrize("name,password", [(name, password)])
def test_login(is_client, name, password):
    response = is_client.authenticate(
        name,
        password
    )
    assert response.status_code == 200
    assert "token" in response.json()
    return response


# @pytest.mark.parametrize("name,password", [(name, password)])
# def test_userinfo(is_client, name, password):
#     response = test_login(is_client, name, password)
#     token = response.json()['token']
#     print(token)

#     response = is_client.userinfo(token)
#     print(response.json())


@pytest.mark.parametrize("name", [(name)])
def test_username_exists(is_client, name):
    response = is_client.username_exists(name)

    assert response == True
