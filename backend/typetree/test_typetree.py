# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import uuid
from urllib.parse import urlparse
from fastapi.testclient import TestClient

from typetree.models import ItemType
from cx.main import app
from typetree.typetree_private import *

client = TestClient(app)


def test_create_and_update_item_type():
    type_name = str(uuid.uuid4())

    # insert
    r = client.post("/ItemType", json={
        "type_details": {
            "type_name": type_name,
            "version": "1.0"
        }
    })

    assert r.status_code == 200
    j = r.json()
    assert 'node' in j
    assert 'id' in j['node']
    assert 'type_details' in j
    assert j['type_details']['type_name'] == type_name
    id1 = j['node']['id']
    
    # update
    r = client.post("/ItemType", json={
        "type_details": {
            "type_name": type_name,
            "version": "2.0"
        }
    })

    assert r.status_code == 200
    j = r.json()
    id2 = j['node']['id']

    assert id1 != id2

    # fetch from id2 and check if 'previous' links to id1
    assert 'previous' in j['node']['node']
    assert j['node']['node']['previous'] == id1

    # update 2
    # update on a given 'previous' id, in this case based from 1st insert
    # basically overruling the internal database head for the type
    # this creates a separate branch version 1.0 -> 3.0
    r = client.post("/ItemType", json={
        "previous": id1,
        "type_details": {
            "type_name": type_name,
            "version": "3.0"
        }
    })

    assert r.status_code == 200
    j = r.json()
    id3 = j['node']['id']

    assert id3 != id1
    assert id3 != id2

    # 'previous' link should point to id1 in this case
    assert j['node']['node']['previous'] == id1



