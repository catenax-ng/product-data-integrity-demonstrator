# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import json
from time import sleep
import requests
import pytest
import os
#import pytest_asyncio
from urllib.parse import urlparse

from .main import app, get_settings
from typetree.dependencies import Settings, settings
from fastapi.testclient import TestClient

from typetree.ssi_state_helper import StateConnectionDidPresentationRequestReceived, StateConnectionFinal, StateMachine

from .ssi_test_templates import *

MOCK_ACAPY = (os.getenv('MOCK_ACAPY', 'False') == 'True')
MOCKED_CONNECTION_ID = "conn1"

def get_settings_override():
    return Settings(acapy_webhook_url="/webhook")


app.dependency_overrides[get_settings] = get_settings_override

class MockResponse:
    def __init__(self, data:dict, status_code:int = 200) -> None:
        self.data = data
        self.status_code = status_code
    @staticmethod
    def from_text(text:str):
        data = json.loads(text)
        return MockResponse(data=data)

    def json(self):
        return self.data

def mock_post_get(*args, **kwargs):
    """
    We mock all methods in one here, post and get, just based on the path
    """
    url = args[0]
    path = urlparse(url).path
    input = kwargs.get('json', {})
    print(path)
    # more specific matches first...
    if path.startswith('/connections/create-invitation'):
        return MockResponse.from_text(CREATE_INVITATION_RESPONSE)
    elif path.startswith('/connections/receive-invitation'):
        return MockResponse.from_text(RECEIVE_INVITATION_RESPONSE)
    elif path.startswith('/connections/'): # with id behind...
        # assuming the get for a specifict connection
        return MockResponse.from_text(CONNECTION_DETAILS_RESPONSE)
    elif path.startswith('/connections'): # no trailing slash, get the list
        return MockResponse.from_text(CONNECTIONS_RESPONSE)
    elif path.startswith('/issue-credential-2.0/send'):
        return MockResponse.from_text(ISSUE_CREDENTIAL_2_SEND_RESPONSE)
    elif path.startswith('/present-proof-2.0/send-request'):
        return MockResponse.from_text(PRESENT_PROOF_2_SEND_REQUEST_RESPONSE)
    elif path.startswith('/present-proof-2.0/records'):
        return MockResponse.from_text(PRESENT_PROOF_2_RECORDS_RESPONSE)
    else:
        print(__name__, 'path unknown:', path)

@pytest.fixture()
def client1():
    with TestClient(app) as client:
        yield client

@pytest.fixture()
def client2():
    with TestClient(app) as client:
        yield client


def test_connection(client1, client2, monkeypatch):
        if MOCK_ACAPY:
            monkeypatch.setattr(requests, 'post', mock_post_get)
            monkeypatch.setattr(requests, 'get', mock_post_get)

        invitation = client1.get('/connections/create-invitation').json() # active participant
        result = client2.post('/connections/receive-invitation', json=invitation['invitation']).json() # passive participant

        connection_id = invitation['connection_id']
        if MOCK_ACAPY:
            connection_id=MOCKED_CONNECTION_ID

        sleep(5) # to let the connection establish
        sm = StateMachine.from_storage(connection_id=connection_id)
        sm.run()

        result = client1.get('/connection-states').json()
        conn = result[connection_id]            
        assert conn['connection_id'] == connection_id
        assert conn['state'] == StateConnectionDidPresentationRequestReceived.NAME
        # how to do in mocked env?

        sleep(5) # to let client2 send the requested presentation
        sm = StateMachine.from_storage(connection_id=connection_id)
        sm.run()

        result = client1.get('/connection-states').json()
        conn = result[connection_id]            
        assert conn['connection_id'] == connection_id
        assert conn['state'] == StateConnectionFinal.NAME

