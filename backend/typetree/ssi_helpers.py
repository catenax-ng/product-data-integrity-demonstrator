# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

from supplytree.supplytreee_helper import parse_data_from_url, parse_node_from_url
from .dependencies import settings, get_acapy_access_token, get_db_name_ssi
import requests
import shelve
from uuid import uuid4
import json
from datetime import datetime

def prepare_headers_from_token(token: str) -> str:
    headers = {
        "Authorization": 'Bearer ' + token
    }
    return headers

def prepare_headers(tenant: str):
    token = get_acapy_access_token(tenant=tenant)
    return prepare_headers_from_token(token=token)


OUR_DID = ''
def get_our_did(tenant: str):
    global OUR_DID
    if not OUR_DID:
        with shelve.open(get_db_name_ssi(tenant), 'r') as db:
            OUR_DID = db['did']
    return OUR_DID

def prefix_did(did):
    if not did.startswith('did:sov:'):
        did = 'did:sov:' + did
    return did

def send_nonce_credential(connection_id:str, tenant: str, nonce: str ="", did: str = ""):
    """
    Sends a credential to the given connection_id that contains a simple
    BearerToken, but the idea is the given nonce that needs to be confirmed
    to find out whether the other end of the connection is in possesion of the
    did:key.
    This is a workaround because connections do not show the did:key behind,
    because the generate separte did:peer (or local did:sov) for every
    new connection.
    nonce: if not given will uuid4 is generated
    did: our did. if not given, read from wallet
    """

    if not nonce:
        nonce = str(uuid4())

    if not did:
        did = get_our_did(tenant=tenant)

    input_template = """
        {
        "connection_id": "",
        "filter": {
            "ld_proof": {
            "credential": {
                "@context": [
                "https://www.w3.org/2018/credentials/v1",
                {
                    "st": "http://supplytree.org/ns#",
                    "BearerCredential": "st:BearerCredential",
                    "nonce": "st:Nonce"
                }
                ],
                "type": [
                "VerifiableCredential",
                "BearerCredential"
                ],
                "issuer": "",
                "issuanceDate": "",
                "nonce": "",
                "credentialSubject": {}
            },
            "options": {
                "proofType": "Ed25519Signature2018"
            }
            }
        }
        }
    """
    input = json.loads(input_template)
    input['connection_id'] = connection_id
    input['filter']['ld_proof']['credential']['nonce'] = nonce
    timestamp = datetime.now().isoformat(timespec='seconds')
    input['filter']['ld_proof']['credential']['issuanceDate'] = timestamp
    input['filter']['ld_proof']['credential']['issuer'] = did
    print(input)

    r = requests.post(settings.acapy_api + '/issue-credential-2.0/send', json=input, headers=prepare_headers(tenant=tenant))
    if r.status_code:
        j = r.json()
        return j
    
    return None


def check_data_content(node_id: str, data_id: str, data_type: str, data_key: str, data_value:str, tenant: str):
    """
    Check whether the given data exists in the given node/data structure
    Returns True if it does
    Returns False in all other cases
    """
    node = parse_node_from_url(node_id, tenant=tenant)
    for d in node.data:
        if d.url == data_id:
            if d.type == data_type:
                data = parse_data_from_url(data_id, tenant=tenant)
                if data_key in data:
                    if data[data_key] == data_value:
                        return True
    # in all other cases
    return False

