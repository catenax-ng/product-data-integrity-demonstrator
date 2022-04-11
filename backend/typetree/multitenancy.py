# Copyright (c) 2022 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/catenax-ng/product-data-integrity-demonstrator
#
# SPDX-License-Identifier: Apache-2.0

import asyncio
import shelve
import secrets, os
import requests
from uuid import uuid4
from fastapi import APIRouter

from typetree.ssi_helpers import prepare_headers, prepare_headers_from_token
from .dependencies import get_acapy_access_token, get_db_name_multitenancy, get_db_name_ssi, get_typetree_base_url, get_webhook_base_url, settings
from .models import ConfigPost, Theme
from supplytree.dependencies import get_reference_directory, get_cache_directory, get_data_directory, get_next_node_directory, get_data_tmp_directory, get_node_directory


router = APIRouter(tags=['Multitenancy'])

async def create_tenant_directories(tenant: str):
    dir = get_reference_directory(tenant)
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir = get_cache_directory(tenant)
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir = get_node_directory(tenant)
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir = get_next_node_directory(tenant)
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir = get_data_directory(tenant)
    if not os.path.exists(dir):
        os.makedirs(dir)
    dir = get_data_tmp_directory(tenant)
    if not os.path.exists(dir):
        os.makedirs(dir)

async def create_sub_wallet(tenant: str):
    if not settings.acapy_api:
        print('ACAPY_API not given, not creating sub-wallets')
        return

    dbname = get_db_name_ssi(tenant=tenant)
    # we use separate dbs to not get access problems
    # yes, we should use proper DB in the future :-)
    with shelve.open(dbname) as db:
        # some structures init
        if not 'connections' in db:
            db['connections'] = {}
        if not 'connections_nonce_sent' in db:
            db['connections_nonce_sent'] = {}

        if not 'wallet_id' in db:
            # try to create a new wallet
            db['wallet_name'] = str(uuid4())
            db['wallet_key'] = str(uuid4())

            input = {
                "wallet_name": db['wallet_name'],
                "wallet_key": db['wallet_key'],
                "wallet_type": "indy"
            }
            # since we are running behind uvicorn or nginx or all inside docker, it can NOT be deteced
            # automatically and needs to be set in env vars
            webhook_url = get_webhook_base_url(tenant=tenant) + '/agent/webhook'
            input['wallet_webhook_urls'] = [
                webhook_url
            ]
            r = requests.post(settings.acapy_api + '/multitenancy/wallet', json=input)
            j = r.json()
            db['wallet_token'] = j['token']
            db['wallet_id'] = j['wallet_id']

            print('wallet_token: ' + j['token'])

        header = prepare_headers_from_token(token=db['wallet_token'])

        if ('wallet_id' in db) and (not 'did' in db):
            # try to create a new did
            input = {
                "method": "sov",
                "options": {
                    "key_type": "ed25519"
                }
            }
            r = requests.post(settings.acapy_api + '/wallet/did/create', json=input, headers=header)
            j = r.json()
            db['did'] = j['result']['did']
            db['verkey'] = j['result']['verkey']
        if ('did' in db) and ('did_register_nym' not in db):
            params = {
                "did": db['did'],
                "verkey": db['verkey']
            }
            j = requests.post(settings.acapy_api + '/ledger/register-nym', params=params).json() # this execution is on the base wallet - don't set headers!
            if j['success'] == True:
                db['did_register_nym'] = True

        if ('did_register_nym' in db) and ('did_published' not in db):
            params = {
                "did": db['did']
            }
            j = requests.post(settings.acapy_api + '/wallet/did/public', params=params, headers=header).json()
            if j['result']['posture'] in ['posted', 'public']:
                db['did_published'] = True



@router.post('/tenant')
async def create_new_tenant():
    """
    Creates a random new tenant id an checks the db if it exists
    returns the tenant_id
    """
    dbname = get_db_name_multitenancy()
    with shelve.open(dbname) as db:
        while(True):
            tenant_id = secrets.token_hex(3)
            if not tenant_id in db:
                default = ConfigPost()
                db[tenant_id] = default
                loop = asyncio.get_event_loop()
                loop.create_task(create_tenant_directories(tenant=tenant_id))
                loop.create_task(create_sub_wallet(tenant=tenant_id))
                return {'tenant': tenant_id }
