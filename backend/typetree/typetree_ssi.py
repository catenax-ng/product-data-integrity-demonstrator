# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import shelve
import requests
import json
from datetime import datetime
from uuid import uuid4
import asyncio

from .ssi_state_helper import ShelveStorage, StateMachine

from .dependencies import ACAPY_API, ORGANIZATION_NAME, settings, get_db_name_ssi
from .ssi_helpers import check_data_content, get_our_did, prepare_headers, prefix_did
from .ssi_templates import CO2_PRESENTATION_REQUEST, ISSUE_SEND_REQUEST, ISSUE_SEND_REQUEST_CO2, CO2_PRESENTATION_REQUEST_SEND
from .co2 import get_co2_sum


router = APIRouter(tags=['TypeTree SSI Private'])



@router.get('/{tenant}/wallet/info')
def get_wallet_info(tenant: str):
    dbname = get_db_name_ssi(tenant=tenant)
    with shelve.open(dbname, 'r') as db:
        did = ''
        if 'did' in db:
            did = db['did']
        return {
            'wallet_name': db['wallet_name'],
            'wallet_id': db['wallet_id'],
            'did': did,
            'verkey': db.get('verkey', ''),
            'did_register_nym': db.get('did_register_nym', ''),
            'did_published': db.get('did_published', ''),
            'wallet_token': db.get('wallet_token', ''), # TODO: security: in production?
        }

def get_connection_details(connection_id: str):
    r = requests.get(ACAPY_API + '/connections/' + connection_id)
    j = r.json()
    return j

#@router.get('/connections/create-invitation')
def create_invitation(tenant: str):
    input = {"my_label": ORGANIZATION_NAME}
    r = requests.post(ACAPY_API + '/connections/create-invitation', json=input, headers=prepare_headers(tenant=tenant))
    j = r.json()
    return j

#@router.post('/connections/receive-invitation')
def receive_invitation(invitation: dict, tenant: str):
    r = requests.post(ACAPY_API + '/connections/receive-invitation', json=invitation, headers=prepare_headers(tenant=tenant))
    j = r.json()
    return j

class ConnectRequest(BaseModel):
    did: str
    alias: str = ''

@router.post('/{tenant}/connect')
def connect(tenant: str, connectRequest: ConnectRequest = Body(...)):
    params = {
        "their_public_did": connectRequest.did,
        "alias": connectRequest.alias,
        "use_public_did": "true",
    }
    j = requests.post(ACAPY_API + '/didexchange/create-request', params=params, headers=prepare_headers(tenant=tenant)).json()
    return j

@router.get('/{tenant}/connections')
def get_connections(tenant: str):
    r = requests.get(ACAPY_API + '/connections', headers=prepare_headers(tenant=tenant))
    j = r.json()
    return j['results']

@router.get('/{tenant}/connection-states')
def get_connection_states(tenant: str):
    connections = get_connections()
    storage = ShelveStorage()
    items = {}
    for conn in connections:
        id = conn['connection_id']
        state_data = storage.get(id)
        state = state_data.get('state', '')
        items[id] = {'connection_id': id, 'state': state}
    return items


@router.get('/{tenant}/wallet/credentials')
def get_credentials(tenant: str):
    r = requests.post(ACAPY_API + '/credentials/w3c', json={}, headers=prepare_headers(tenant=tenant))
    j = r.json()
    result = []
    for cred in j['results']:
        result.append(cred)
    return result

@router.get('/{tenant}/wallet/credential/{record_id}')
def get_credential(record_id: str, tenant: str):
    j = requests.get(ACAPY_API + '/credential/w3c/' + record_id, headers=prepare_headers(tenant=tenant)).json()
    return j

@router.post('/{tenant}/wallet/credential/{record_id}/send')
def send_credential(tenant: str, record_id: str, msg: dict = Body(...)):
    return
    connection_id = msg['connection_id']
    j = requests.post(ACAPY_API + '/present-proof-2.0/send-proposal', headers=prepare_headers(tenant=tenant)).json()

class Co2SumPresentationRequest(BaseModel):
    node_id: str
    connection_id: str

@router.post('/{tenant}/wallet/presentation/request/co2sum')
def send_presentation_request_co2sum(tenant: str, co2request: Co2SumPresentationRequest = Body(...)):
    """
    Request a VP containing the sum of CO2 values along the chain, starting with the given node_id
    """
    connection_id = co2request.connection_id
    node_id = co2request.node_id
    input = json.loads(CO2_PRESENTATION_REQUEST)
    input['connection_id'] = connection_id
    input['presentation_request']['dif']['presentation_definition']['id'] = str(uuid4())
    input['presentation_request']['dif']['presentation_definition']['input_descriptors'][0]['constraints']['fields'][0]['filter']['pattern'] = node_id
    j = requests.post(ACAPY_API + '/present-proof-2.0/send-request',json=input, headers=prepare_headers(tenant=tenant)).json()
    return j

@router.get('/{tenant}/wallet/presentation-requests')
def get_presentation_requests_received(tenant: str, state: str = ''):
    """
    state: must be in ['propsal-sent', 'proposal-received', 'request-sent', 'request-received', 'presentation-sent', 'presentation-received', 'done', 'abondoned']
    """
    possible_states = ['', 'propsal-sent', 'proposal-received', 'request-sent', 'request-received', 'presentation-sent', 'presentation-received', 'done', 'abondoned']
    if state not in possible_states:
        raise HTTPException(400, "state must be in: " + possible_states)
    params = None
    if state:
        params = {
            'state': state,
        }
    j = requests.get(ACAPY_API + '/present-proof-2.0/records', params=params, headers=prepare_headers(tenant=tenant)).json()
    return j['results']

@router.get('/{tenant}/wallet/presentation-request/{record_id}')
def get_presentation_request(tenant: str, record_id: str):
    j = requests.get(ACAPY_API + '/present-proof-2.0/records/' + record_id, headers=prepare_headers(tenant=tenant)).json()
    return j

@router.get('/{tenant}/wallet/presentation-request/{record_id}/credentials')
def get_presentation_request_credentials(tenant: str, record_id: str):
    """
    Returns all credentials that map the request
    """
    j = requests.get(ACAPY_API + '/present-proof-2.0/records/' + record_id + '/credentials', headers=prepare_headers(tenant=tenant)).json()
    # restructure. acapy should be fixed here
    result = []
    for item in j:
        cred_value = {**item}
        del cred_value['record_id']
        obj = {
            'record_id': item['record_id'],
            'cred_value': cred_value,
        }
        result.append(obj)

    return result

@router.post('/{tenant}/wallet/presentation-request/{record_id}/send/{credential_id}')
def send_presentation_request_credential(tenant: str, record_id: str, credential_id: str):
    params = json.loads(CO2_PRESENTATION_REQUEST_SEND)
    params['dif']['record_ids']['co2_sum'] = [credential_id]
    j = requests.post(ACAPY_API + '/present-proof-2.0/records/' + record_id + '/send-presentation', json=params, headers=prepare_headers(tenant=tenant)).json()
    return j

@router.get('/{tenant}/wallet/presentations-received')
def get_presentations_received(tenant: str):
    """
    Returns all presentations that we received and we are verifiers for and which are finished (done)
    """
    params = {
        'role': 'verifier',
        'state': 'done',
    }
    j = requests.get(ACAPY_API + '/present-proof-2.0/records', params=params, headers=prepare_headers(tenant=tenant)).json()
    return j['results']

def extract_did_identifier(doc: dict) -> str:
    """
    If contains "proof.verificationMethod" it extracts the did from there and deletes the did method prefix
    It remains the identifier part of the DID
    """
    ver_method = doc['proof']['verificationMethod']
    did = ver_method.split('#')[0]
    did_identifier_part = did.split(':')[-1]
    return did_identifier_part


def fetch_verkey(tenant: str, did_identifier: str) -> str:
    """
    Loads the verkey from the ledger for a given DID
    """
    params = {
        'did': did_identifier
    }
    j = requests.get(ACAPY_API + '/ledger/did-verkey', params=params, headers=prepare_headers(tenant=tenant)).json()
    verkey = j['verkey']

    return verkey

def verify_doc(tenant: str, doc: dict, verkey: str) -> bool:
    """
    Uses the acapy API to verify a document.
    verkey: the verkey (public key) of the signature. It needs to be fetched in another way before this call
    """
    input = {
        'doc': doc,
        'verkey': verkey,
    }
    r = requests.post(ACAPY_API + '/jsonld/verify', json=input, headers=prepare_headers(tenant=tenant))
    j = r.json()
    return j['valid']

@router.post('/{tenant}/wallet/verify')
def verify(tenant: str, doc: dict = Body(...)):
    """
    Inut is a doc that contains a proof and/or a sub group of "verifiableCredentials" and if so,
    all items in there are verified as well.
    Remark: we check the signature, but not the proofPurpose (and I think the used acapy method also does not do this)
    """
    result = {
        'presentation_verified': False
    }
    pres_did = extract_did_identifier(doc=doc)
    pres_verkey = fetch_verkey(tenant=tenant, did_identifier=pres_did)
    pres_verified = verify_doc(tenant=tenant, doc=doc, verkey=pres_verkey)
    if(pres_verified):
        result['presentation_verified'] = True
    
    credentials = doc['verifiableCredential']
    vc_valid = []
    all_vc_valid = True
    for vc in credentials:
        vc_did = extract_did_identifier(vc)
        vc_verkey = fetch_verkey(tenant=tenant, did_identifier=vc_did)
        vc_verified = verify_doc(tenant=tenant, doc=vc, verkey=vc_verkey)
        if vc_verified:
            vc_valid.append(True)
        else:
            vc_valid.append(False)
            all_vc_valid = False

    result['verifiable_credentials_verified'] = vc_valid
    result['all_vcs_verified'] = all_vc_valid
    return result



# @router.get('/wallet/credentials/plain')
def get_credentials_plain(tenant: str):
    credentials = get_credentials(tenant=tenant)
    items = []
    for cred in credentials:
        items.append(cred['cred_value'])
    return items

class DataProof(BaseModel):
    nodeId: str = ''
    dataId: str = ''
    dataType: str = ''
    dataKey: str = ''
    dataValue: str = ''
    class Config:
        schema_extra = {
            "example": {
                "nodeId": "http://localhost:8000/node/bd6efcaddb152130c45ce3f8f2e322f169d8cf1fa186d3424bb87d4b44ea723e",
                "dataId": "http://localhost:8000/data/7c08fd717a6a4e54a5b17e4b610080efeaefba9e95ff583dbaffeb1b4906f987",
                "dataType": "http://supplytree.org/ns/ItemType",
                "dataKey": "version",
                "dataValue": "2"
            }
        }
class DataProofRequest(BaseModel):
    data_proof: DataProof
    connection_id: str

@router.post('/{tenant}/request-data-attestation')
def request_data_attestation(data_proof_request: DataProofRequest, tenant: str):
    """
    Request a general attestation of a data attribute (Verifiable Credential Request)
    """
    our_did = prefix_did(get_our_did(tenant=tenant))
    # create an issue proposal
    input = json.loads(ISSUE_SEND_REQUEST)
    input['connection_id'] = data_proof_request.connection_id
    input['filter']['ld_proof']['credential']['credentialSubject'] = data_proof_request.data_proof.dict()
    input['filter']['ld_proof']['credential']['credentialSubject']['id'] = our_did
    timestamp = datetime.now().isoformat(timespec='seconds')
    input['filter']['ld_proof']['credential']['issuanceDate'] = timestamp
    input['holder_did'] = our_did
    r = requests.post(settings.acapy_api + '/issue-credential-2.0/send-request', json=input, headers=prepare_headers(tenant=tenant))
    if r.status_code == 200:
        j = r.json()
        return j
    return None

class Co2ChainProof(BaseModel):
    nodeId: str
    co2Sum: str

class Co2ChainProofRequest(BaseModel):
    proof: Co2ChainProof
    connection_id: str

@router.post('/{tenant}/request-co2-attestation')
def request_co2_attestation(proof_request: Co2ChainProofRequest, tenant: str):
    """
    Init VC issuing request for CO2 (issuer should walk the tree to sum up all values)
    """
    our_did = prefix_did(get_our_did(tenant=tenant))
    # create an issue proposal
    input = json.loads(ISSUE_SEND_REQUEST_CO2)
    input['connection_id'] = proof_request.connection_id
    input['filter']['ld_proof']['credential']['credentialSubject'] = proof_request.proof.dict()
    input['filter']['ld_proof']['credential']['credentialSubject']['id'] = our_did
    timestamp = datetime.now().isoformat(timespec='seconds')
    input['filter']['ld_proof']['credential']['issuanceDate'] = timestamp
    input['holder_did'] = our_did
    r = requests.post(settings.acapy_api + '/issue-credential-2.0/send-request', json=input, headers=prepare_headers(tenant=tenant))
    if r.status_code == 200:
        j = r.json()
        return j
    return None


async def do_later(connection_id:str):
    # await asyncio.sleep(5)
    sm = StateMachine.from_storage(connection_id=connection_id)
    sm.run()

async def issue_cred(cred_ex_id, connection_id, tenant: str):
    # TODO: check content
    did = prefix_did(get_our_did(tenant=tenant))
    r = requests.get(settings.acapy_api + '/issue-credential-2.0/records/' + cred_ex_id, headers=prepare_headers(tenant=tenant))
    if r.status_code != 200:
        print('record not found (expected in many cases):', cred_ex_id)
        return

    j = r.json()
    vc_req = j['cred_ex_record']['by_format']['cred_request']['ld_proof']['credential']
    vc_req['issuer'] = did
    vc_req['issuanceDate'] = datetime.now().isoformat(timespec='seconds')
    # vc_req['credentialSubject']['id'] = vc_req['credentialSubject']['nodeId'] # TODO: does this make sense?

    input = None
    # before we send, let's check the content!
    if 'ContentConfirmationCredential' in vc_req['type']:
        node_id = vc_req['credentialSubject']['nodeId']
        data_id = vc_req['credentialSubject']['dataId']
        data_type = vc_req['credentialSubject']['dataType']
        data_key = vc_req['credentialSubject']['dataKey']
        data_value = vc_req['credentialSubject']['dataValue']
        if not check_data_content(node_id=node_id, data_id=data_id, data_type=data_type, data_key=data_key, data_value=data_value, tenant=tenant):
            print('Error: can not confirm requested credential data! Decline issuing the VC. cred_ex_id: ' + cred_ex_id)
            # TODO: formally decline the request
            return
        
        input = json.loads(ISSUE_SEND_REQUEST)
        input['filter']['ld_proof']['credential'] = vc_req

    elif 'Co2ConfirmationCredential' in vc_req['type']:
        co2_sum = get_co2_sum(vc_req['credentialSubject']['nodeId'], tenant=tenant)
        vc_req['credentialSubject']['co2Sum'] = str(co2_sum)
        input = json.loads(ISSUE_SEND_REQUEST_CO2)
        input['filter']['ld_proof']['credential'] = vc_req

    else:
        raise Exception("Don't know credential type. Can NOT issue a credential. type: " + vc_req['type'])

    # original request no longer needed
    requests.delete(settings.acapy_api + '/issue-credential-2.0/records/' + cred_ex_id, headers=prepare_headers(tenant=tenant))

    input['connection_id'] = connection_id

    r = requests.post(settings.acapy_api + '/issue-credential-2.0/send', json=input, headers=prepare_headers(tenant=tenant))
    print(r.status_code)
    print(r.json())

@router.post('/{tenant}/agent/webhook/topic/{topic:path}')
async def agent_webhook(topic:str, tenant: str, message:dict = Body(...)):
    """
    This webhook receives ALL updates from acapy (the agent / wallet part).

    Based on the 'topic' different messages and in consequence actions follow.
    """
    print(topic)
    #print(message)
    if topic.startswith('connections/'):
        connection_id = message['connection_id']
        # asyncio.create_task(do_later(connection_id))
    if topic.startswith('issue_credential_v2_0/'):
        print(message)
        if (message.get('role', '') == 'issuer') and (message.get('state', '') == 'request-received') and (not message.get('initiator', '') == 'self'):
            cred_ex_id = message['cred_ex_id']
            connection_id = message['connection_id']
            asyncio.create_task(issue_cred(cred_ex_id=cred_ex_id, connection_id=connection_id, tenant=tenant))
    if topic.startswith('issue_credential_v2_0_ld_proof/'):
        print(message)
    if topic.startswith('present_proof_v2_0/'):
        print(message)
    
